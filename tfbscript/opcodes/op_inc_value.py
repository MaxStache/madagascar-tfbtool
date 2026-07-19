from dataclasses import dataclass, field

from tfbscript.ansi import operator
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("inc value")
@dataclass
class OpIncValue(Opcode):
    lhs: Reference = field(default_factory=Reference)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpIncValue":
        return cls(lhs=reader.read_reference())

    def source_line(self, inline: bool = False) -> str:
        return f"{self.lhs} {operator('++')};"
