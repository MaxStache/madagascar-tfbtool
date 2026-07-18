from dataclasses import dataclass, field

from TFBStringTable import TFBStringTable
from utils.binaryReader import PayloadBinaryReader


@dataclass
class InstructionFlags:
    flowControl: int = 0  # bits 0-2 — flow-control value returned by FUN_00431130
    # 0: return - skip to end of script (block)
    # 1: continue - proceed normally
    # 2,3,4.... : break  -  skip the rest of N-1 enclosing levels, then resume normally one level further up.
    reservedLow: int = 0  # bits 3-5  — unknown / reserved
    noHandler: bool = False  # bit 6     — no handler bound (loader skips construction) (aka disabled at runtime)
    runtimeScratch: bool = (
        False  # bit 7     — runtime-only scratch flag (always 0 on disk)
    )
    noElse: bool = False  # bit 8     — IF instruction has no ELSE branch
    reservedHigh: int = 0  # bits 9-10 — unknown / reserved
    descendantSpan: int = 0  # bits 11-31 — 21-bit descendant span

    reservedHigh: int = 0  # bits 9-10 — unknown / reserved
    descendantSpan: int = 0  # bits 11-31 — 21-bit descendant span

    @staticmethod
    def decode(value: int) -> "InstructionFlags":
        f = InstructionFlags()
        f.flowControl = value & 0x7
        f.reservedLow = (value >> 3) & 0x7
        f.noHandler = bool(value & 0x40)
        f.runtimeScratch = bool(value & 0x80)
        f.noElse = bool(value & 0x100)
        f.reservedHigh = (value >> 9) & 0x3
        f.descendantSpan = (value >> 11) & 0x1FFFFF
        return f

    def encode(self) -> int:
        v = 0
        v |= self.flowControl & 0x7
        v |= (self.reservedLow & 0x7) << 3

        if self.noHandler:
            v |= 0x40
        if self.runtimeScratch:
            v |= 0x80
        if self.noElse:
            v |= 0x100

        v |= (self.reservedHigh & 0x3) << 9
        v |= (self.descendantSpan & 0x1FFFFF) << 11

        return v

    def flowControlToString(self) -> str:
        if self.flowControl == 0:
            return "stop"  # return
        elif self.flowControl == 1:
            return "continue"
        else:
            return f"break {self.flowControl - 1}"

    def print(self):
        print("InstructionFlags:")
        print(f"  flowControl:     {self.flowControl}")
        print(f"  reservedLow:     0x{self.reservedLow:X}")
        print(f"  noHandler:       {self.noHandler}")
        print(f"  runtimeScratch:  {self.runtimeScratch}")
        print(f"  noElse:          {self.noElse}")
        print(f"  reservedHigh:    0x{self.reservedHigh:X}")
        print(f"  descendantSpan:  {self.descendantSpan}")


@dataclass
class OpParserContext:
    opcodeTable: TFBStringTable
    globalRefTable: TFBStringTable
    localRefTable: TFBStringTable
    controlBlockCounter: int = 0


@dataclass
class COpCode:
    _opcodeIndex: int = 0
    flags: InstructionFlags = field(default_factory=InstructionFlags)
    _payloadSize: int = 0
    _rawPayload: bytes = b""

    thenInstructions: list["COpCode"] = field(
        default_factory=list
    )  # {flags.descendantSpan} instructions

    def totalSpan(self) -> int:
        """
        Total flattened count of this instruction plus all of its descendants
        (children, grandchildren, ...), matching the on-disk descendantSpan encoding.
        """
        return 1 + sum(child.totalSpan() for child in self.thenInstructions)

    @classmethod
    def read(
        cls,
        reader,
        context: OpParserContext,
    ):
        """
        Reads an opcode from a binary reader
        """
        from . import (
            OPCODE_REGISTRY,
            COpShutdown,
            COpStartup,
            COpPrescript,
            COpBehaviorImplementation,
        )

        opcodeIndex = reader.readUint8()
        flagsValue = reader.readUint32()
        flags = InstructionFlags.decode(flagsValue)
        _payloadSize = reader.readUint8()

        behaviorEntry = None

        if opcodeIndex == 0xFF:
            # Control block opcode, determine which one based on the controlBlockCounter
            if context.controlBlockCounter == 0:
                opcodeClass = COpPrescript
            elif context.controlBlockCounter == 1:
                opcodeClass = COpStartup
            elif context.controlBlockCounter == 2:
                opcodeClass = COpShutdown
            else:
                behaviors = context.localRefTable.getAllWithType(
                    "behavior"
                )  # abc::behavior, test::behavior, etc...
                behavior_idx = context.controlBlockCounter - 3

                behaviorEntry = behaviors[behavior_idx]
                opcodeClass = COpBehaviorImplementation

            context.controlBlockCounter += 1
        else:
            # Lookup the opcode class in the opcode table
            if opcodeIndex >= len(context.opcodeTable.entries):
                raise ValueError(f"Invalid opcode index: {opcodeIndex}")

            opcodeName = context.opcodeTable.entries[opcodeIndex].string
            opcodeName = opcodeName.split("::")[0]  # my op::op-code -> my op

            if opcodeName not in OPCODE_REGISTRY:
                raise ValueError(f"Unknown opcode name: {opcodeName}")

            opcodeClass = OPCODE_REGISTRY[opcodeName]

        _rawPayload = reader.readBytes(_payloadSize)
        payloadReader = PayloadBinaryReader(
            _rawPayload,
            context.globalRefTable,
            context.localRefTable,
            littleEndian=True,
        )

        # Read the specific opcode payload data
        opcodeClassInst = opcodeClass.readPayload(payloadReader, flags)

        opcodeClassInst._opcodeIndex = opcodeIndex
        opcodeClassInst._payloadSize = _payloadSize
        opcodeClassInst.flags = flags
        opcodeClassInst._rawPayload = _rawPayload

        if isinstance(opcodeClassInst, COpBehaviorImplementation):
            opcodeClassInst._behaviorEntry = behaviorEntry

        descendantsRead = 0
        while descendantsRead < flags.descendantSpan:
            childInstr = COpCode.read(reader, context)
            opcodeClassInst.thenInstructions.append(childInstr)
            descendantsRead += childInstr.totalSpan()

        return opcodeClassInst

    def print(self, indent=0):
        indent_str = " " * 4 * indent

        print(f"{indent_str}{self.toString()}")

        for child in self.thenInstructions:
            child.print(indent + 1)

    # IMPLEMENT THE FOLLOWING METHOD IN SUBCLASSES TO PROVIDE CUSTOM PRINTING
    # def toString(self) -> str:
    #     return "MY OPCODE, abc bca"

    def toString(self) -> str | None:
        return f"{self.__class__.__name__}, payload: {self._rawPayload.hex() if self._rawPayload else '-'}"
