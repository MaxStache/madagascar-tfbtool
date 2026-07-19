from dataclasses import dataclass, field

from tfbscript.ansi import keyword, operator
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference
from tfbscript.rhs import Rhs


@opcode("set value")
@dataclass
class OpSetValue(Opcode):
    lhs: Reference = field(default_factory=Reference)
    rhs: Rhs = field(default_factory=Rhs)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpSetValue":
        return cls(lhs=reader.read_reference(), rhs=reader.read_rhs())

    def source_line(self, inline: bool = False) -> str:
        return f"{keyword('set')} {self.lhs} {operator('=')} {self.rhs};"
