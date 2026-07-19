"""Instruction flags, parser context, opcode registry and the Opcode base class."""

import sys
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from tfbscript.payload import PayloadReader
from tfbscript.string_table import StringTable

if TYPE_CHECKING:
    from tfbscript.binary import BinaryReader


@dataclass
class InstructionFlags:
    """The 32-bit flags word that follows every opcode index."""

    flow_control: int = 0  # bits 0-2 -- flow-control value returned by FUN_00431130
    # 0: return - skip to end of script (block)
    # 1: continue - proceed normally
    # 2,3,4...: break - skip the rest of N-1 enclosing levels, then resume
    #           normally one level further up.
    reserved_low: int = 0  # bits 3-5   -- unknown / reserved
    no_handler: bool = False  # bit 6   -- no handler bound (loader skips construction) (aka disabled at runtime)
    runtime_scratch: bool = False  # bit 7 -- runtime-only scratch flag (always 0 on disk)
    no_else: bool = False  # bit 8     -- IF instruction has no ELSE branch
    reserved_high: int = 0  # bits 9-10 -- unknown / reserved
    descendant_span: int = 0  # bits 11-31 -- 21-bit descendant span

    @staticmethod
    def decode(value: int) -> "InstructionFlags":
        return InstructionFlags(
            flow_control=value & 0x7,
            reserved_low=(value >> 3) & 0x7,
            no_handler=bool(value & 0x40),
            runtime_scratch=bool(value & 0x80),
            no_else=bool(value & 0x100),
            reserved_high=(value >> 9) & 0x3,
            descendant_span=(value >> 11) & 0x1FFFFF,
        )

    def encode(self) -> int:
        value = self.flow_control & 0x7
        value |= (self.reserved_low & 0x7) << 3
        if self.no_handler:
            value |= 0x40
        if self.runtime_scratch:
            value |= 0x80
        if self.no_else:
            value |= 0x100
        value |= (self.reserved_high & 0x3) << 9
        value |= (self.descendant_span & 0x1FFFFF) << 11
        return value

    def flow_control_str(self) -> str:
        if self.flow_control == 0:
            return "stop"  # return
        if self.flow_control == 1:
            return "continue"
        return f"break {self.flow_control - 1}"


@dataclass
class ParserContext:
    """Shared state while reading a script's instruction stream."""

    opcode_table: StringTable
    global_refs: StringTable
    local_refs: StringTable

    # Counter for 0xFF opcodes, which are control blocks such as OpPrescript,
    # OpStartup, OpShutdown, etc. The Nth occurrence decides whether it is an
    # OpPrescript(0), OpStartup(1), OpShutdown(2) or OpBehaviorImplementation(3,4,5,...).
    control_block_counter: int = 0


# Opcode-table name (e.g. "set value") -> Opcode subclass. Populated by the
# @opcode decorator; importing tfbscript.opcodes registers all implementations.
OPCODE_REGISTRY: dict[str, type["Opcode"]] = {}


def opcode(name: str):
    """Class decorator that registers an Opcode subclass under its table name."""

    def register(cls: type["Opcode"]) -> type["Opcode"]:
        OPCODE_REGISTRY[name] = cls
        return cls

    return register


@dataclass
class Opcode:
    """One instruction; also the generic fallback for unimplemented opcodes."""

    opcode_index: int = 0
    flags: InstructionFlags = field(default_factory=InstructionFlags)
    raw_payload: bytes = b""
    context: ParserContext | None = None

    # The next {flags.descendant_span} instructions in the stream, re-nested.
    children: list["Opcode"] = field(default_factory=list)

    def total_span(self) -> int:
        """Total flattened count of this instruction plus all of its descendants
        (children, grandchildren, ...), matching the on-disk descendant_span encoding.
        """
        return 1 + sum(child.total_span() for child in self.children)

    @classmethod
    def read(cls, reader: "BinaryReader", context: ParserContext) -> "Opcode":
        """Read one instruction (and its re-nested descendants) from the stream."""
        from tfbscript.opcodes.op_behavior_implementation import OpBehaviorImplementation
        from tfbscript.opcodes.op_prescript import OpPrescript
        from tfbscript.opcodes.op_shutdown import OpShutdown
        from tfbscript.opcodes.op_startup import OpStartup

        opcode_index = reader.read_u8()
        flags = InstructionFlags.decode(reader.read_u32())
        payload_size = reader.read_u8()

        behavior_entry = None

        if opcode_index == 0xFF:
            control_blocks = [OpPrescript, OpStartup, OpShutdown]
            if context.control_block_counter < len(control_blocks):
                opcode_class = control_blocks[context.control_block_counter]
            else:
                # abc::behavior, test::behavior, etc...
                behaviors = context.local_refs.all_with_type("behavior")
                behavior_entry = behaviors[context.control_block_counter - 3]
                opcode_class = OpBehaviorImplementation

            context.control_block_counter += 1
        else:
            entry = context.opcode_table.get(opcode_index)
            if entry is None:
                raise ValueError(f"Invalid opcode index: {opcode_index}")

            opcode_name = entry.name  # "my op::op-code" -> "my op"
            opcode_class = OPCODE_REGISTRY.get(opcode_name)
            if opcode_class is None:
                print(
                    f"Unknown opcode name: {opcode_name}, falling back to generic Opcode",
                    file=sys.stderr,
                )
                opcode_class = Opcode

        raw_payload = reader.read_bytes(payload_size)
        payload_reader = PayloadReader(
            raw_payload,
            context.global_refs,
            context.local_refs,
            little_endian=True,
        )

        instruction = opcode_class.parse_payload(payload_reader)
        instruction.opcode_index = opcode_index
        instruction.flags = flags
        instruction.raw_payload = raw_payload
        instruction.context = context

        if isinstance(instruction, OpBehaviorImplementation):
            instruction.behavior_entry = behavior_entry

        descendants_read = 0
        while descendants_read < flags.descendant_span:
            child = Opcode.read(reader, context)
            instruction.children.append(child)
            descendants_read += child.total_span()

        return instruction

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "Opcode":
        """Parse this opcode's payload. Override in subclasses; the base
        implementation is the generic fallback and parses nothing."""
        if cls is not Opcode:
            print(
                f"Warning: parse_payload not implemented for {cls.__name__}. "
                "Returning empty instance.",
                file=sys.stderr,
            )
        return cls()

    def source_line(self, inline: bool = False) -> str:
        """One line of decompiled pseudo-source for this instruction.

        Override in subclasses; the base implementation dumps the raw payload.
        `inline` renders the instruction as an embeddable expression (used by
        if/else conditions) instead of a statement.
        """
        payload = self.raw_payload.hex() if self.raw_payload else "-"
        name = ""
        if self.context is not None:
            name = f"{self.context.opcode_table.entries[self.opcode_index].string}, "
        return f"{name}{type(self).__name__}, payload: {payload}"

    def print_tree(self, indent: int = 0) -> None:
        """Print this instruction and its children as indented pseudo-source."""
        print(f"{'    ' * indent}{self.source_line()}")
        for child in self.children:
            child.print_tree(indent + 1)
