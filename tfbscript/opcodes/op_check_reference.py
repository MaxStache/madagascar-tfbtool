from dataclasses import dataclass, field
from typing import override

from tfbscript.ansi import keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("check reference")
@dataclass
class OpCheckReference(Opcode):
    ref1: Reference = field(default_factory=Reference)
    ref2: Reference = field(default_factory=Reference)


    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpCheckReference":
        ref1 = reader.readRef()
        ref2 = reader.readRef()

        return cls(ref1=ref1, ref2=ref2)

    @override
    def source_line(self, inline: bool = False) -> str:
        condition = f"*{self.ref1} is reference to {self.ref2}"
        if inline:
            return condition

        return f"{keyword('check reference (')} {condition} {keyword(')')}"