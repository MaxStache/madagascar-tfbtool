from dataclasses import dataclass, field

from tfbscript.ansi import func_call, quoted_string
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("print")
@dataclass
class OpPrint(Opcode):
    target: Reference = field(default_factory=Reference)
    content: str = ""

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpPrint":
        target = reader.readRef()
        content = reader.read_string(reader.read_u8())
        return cls(target=target, content=content)

    def source_line(self, inline: bool = False) -> str:
        return func_call("print", str(self.target), quoted_string(self.content))
