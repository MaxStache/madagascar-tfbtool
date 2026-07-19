from dataclasses import dataclass

from tfbscript.opcodes.block import BlockOpcode
from tfbscript.string_table import StringTableEntry


@dataclass
class OpBehaviorImplementation(BlockOpcode):
    # The behavior's entry in the local ref table, resolved by Opcode.read;
    # used for printing.
    behavior_entry: StringTableEntry | None = None

    def block_name(self) -> str:
        name = self.behavior_entry.name if self.behavior_entry else "Failed to resolve"
        return f"Behavior {name}"

    def source_line(self, inline: bool = False) -> str:
        name = self.behavior_entry.name if self.behavior_entry else "Failed to resolve"
        return f"[ Behavior: {name} ]"
