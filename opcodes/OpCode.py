from dataclasses import dataclass, field
from . import OPCODE_REGISTRY
@dataclass
class InstructionFlags:
    reservedLow: int = 0          # bits 0-5  — unknown / reserved
    noHandler: bool = False       # bit 6     — no handler bound (loader skips construction) (aka disabled at runtime)
    runtimeScratch: bool = False  # bit 7     — runtime-only scratch flag (always 0 on disk)
    noElse: bool = False          # bit 8     — IF instruction has no ELSE branch
    reservedHigh: int = 0         # bits 9-10 — unknown / reserved
    descendantSpan: int = 0       # bits 11-31 — 21-bit descendant span

    @staticmethod
    def decode(value: int) -> "InstructionFlags":
        f = InstructionFlags()
        f.reservedLow = value & 0x3F
        f.noHandler = bool(value & 0x40)
        f.runtimeScratch = bool(value & 0x80)
        f.noElse = bool(value & 0x100)
        f.reservedHigh = (value >> 9) & 0x3
        f.descendantSpan = (value >> 11) & 0x1FFFFF
        return f

    def encode(self) -> int:
        v = 0
        v |= self.reservedLow & 0x3F

        if self.noHandler:
            v |= 0x40
        if self.runtimeScratch:
            v |= 0x80
        if self.noElse:
            v |= 0x100

        v |= (self.reservedHigh & 0x3) << 9
        v |= (self.descendantSpan & 0x1FFFFF) << 11

        return v

    def print(self):
        print("InstructionFlags:")
        print(f"  reservedLow:     0x{self.reservedLow:X}")
        print(f"  noHandler:       {self.noHandler}")
        print(f"  runtimeScratch:  {self.runtimeScratch}")
        print(f"  noElse:          {self.noElse}")
        print(f"  reservedHigh:    0x{self.reservedHigh:X}")
        print(f"  descendantSpan:  {self.descendantSpan}")

@dataclass
class COpCode:
    _opcodeIndex: int = 0
    flags: InstructionFlags = field(default_factory=InstructionFlags)
    _payloadSize: int = 0

    @classmethod
    def read(cls, reader, opcodeTable, globalRefTable, localRefTable):
        """
        Reads an opcode from a binary reader
        """
        opcodeIndex = reader.readUint32()
        flagsValue = reader.readUint32()
        flags = InstructionFlags.decode(flagsValue)
        _payloadSize

        # Lookup the opcode class in the opcode table
        if opcodeIndex >= len(opcodeTable.entries):
            raise ValueError(f"Invalid opcode index: {opcodeIndex}")

        opcodeName = opcodeTable.entries[opcodeIndex].string
        if opcodeName not in OPCODE_REGISTRY:
            raise ValueError(f"Unknown opcode name: {opcodeName}")

        opcodeClass = OPCODE_REGISTRY[opcodeName]

        # Read the specific opcode data
        return opcodeClass.readPayload(payloadReader, flags)