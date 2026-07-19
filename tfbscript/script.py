"""The top-level TFB script (.ai) file."""

from dataclasses import dataclass
from pathlib import Path

from tfbscript.binary import BinaryReader
from tfbscript.opcodes import Opcode, ParserContext
from tfbscript.string_table import StringTable


@dataclass
class ScriptFile:
    """A parsed TFB script (.ai) file."""

    magic_string: str
    unk: bytes  # 4 unknown bytes after the magic string

    opcode_table: StringTable
    global_refs: StringTable
    local_refs: StringTable

    instructions: list[Opcode]

    @classmethod
    def read(cls, reader: BinaryReader, debugOptions={}) -> "ScriptFile":
        """Read a ScriptFile from a binary reader."""

        debug_store = {
            "unresolved_ops": set(),
        }

        magic_string = reader.read_string(reader.read_u8())
        unk = reader.read_bytes(4)

        opcode_table = StringTable.read(reader)
        global_refs = StringTable.read(reader)
        local_refs = StringTable.read(reader)

        instruction_count = reader.read_u32()
        context = ParserContext(opcode_table, global_refs, local_refs)

        instructions: list[Opcode] = []
        instructions_read = 0
        try:
            while instructions_read < instruction_count:
                instruction = Opcode.read(reader, context, debug_store=debug_store)
                instructions.append(instruction)
                # Count the instruction and its descendants.
                instructions_read += instruction.total_span()
        except Exception as error:
            raise ValueError(
                f"Error reading instruction {instructions_read}: {error}"
            ) from error
        
        if debugOptions.get("listUnresolvedOps"):
            print(f"Unresolved ops: {debug_store['unresolved_ops']}")

        return cls(magic_string, unk, opcode_table, global_refs, local_refs, instructions)

    @classmethod
    def from_path(cls, path: str | Path, debugOptions={}) -> "ScriptFile":
        """Read a ScriptFile from an .ai file on disk."""
        data = Path(path).read_bytes()
        return cls.read(BinaryReader(data, little_endian=True), debugOptions=debugOptions)

    def print_tree(self) -> None:
        """Print the whole script as indented pseudo-source."""
        for instruction in self.instructions:
            instruction.print_tree()
