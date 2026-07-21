from dataclasses import dataclass, field

from tfbscript.ansi import keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("find variable")
@dataclass
class OpFindVariable(Opcode):
    var_ref: Reference = field(default_factory=Reference)
    owner_ref: Reference = field(default_factory=Reference)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpFindVariable":
        return cls(var_ref=reader.readRef(), owner_ref=reader.readRef())

    def source_line(self, inline: bool = False) -> str:
        return f"{keyword('find variable (')} {self.var_ref} in {self.owner_ref} {keyword(')')}"
