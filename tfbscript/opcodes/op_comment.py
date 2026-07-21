from dataclasses import dataclass

from tfbscript.ansi import comment
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader

@opcode("comment") # TODO: the actual opcode name is "comment:" with a : at end, but the parser is splitting it wrongly to [comment, :op-code]
@dataclass
class OpComment(Opcode):
    content: str = ""

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpComment":
        content = reader.read_string(reader.read_u8())
        return cls(content=content)

    def source_line(self, inline: bool = False) -> str:
        return comment(f"// {self.content}")
