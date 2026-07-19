from dataclasses import dataclass, field

from tfbscript.ansi import keyword, type_
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("create variable")
@dataclass
class OpCreateVariable(Opcode):
    variable: Reference = field(default_factory=Reference)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpCreateVariable":
        return cls(variable=reader.read_reference())

    def source_line(self, inline: bool = False) -> str:
        var_type = self.variable.entry.type if self.variable.entry else "unknown"
        return f"{keyword('var')} {self.variable} : {type_(var_type)};"
