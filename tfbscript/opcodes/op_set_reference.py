from dataclasses import dataclass, field

from tfbscript.ansi import keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("set reference")
@dataclass
class OpSetReference(Opcode):
    dest_ref: Reference = field(default_factory=Reference)
    src_ref: Reference = field(default_factory=Reference)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpSetReference":
        return cls(dest_ref=reader.readRef(), src_ref=reader.readRef())

    def source_line(self, inline: bool = False) -> str:
        return f"{keyword('set reference')} *{self.dest_ref} = {self.src_ref};"
