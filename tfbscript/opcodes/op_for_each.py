from dataclasses import dataclass, field
from typing import override

from tfbscript.ansi import keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.opcodes.enums import SetDirection
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("for each", "Loops over a set in the order of set_direction, stores the current element in [^each]")
@dataclass
class OpForEach(Opcode):
    set_ref: Reference = field(default_factory=Reference)
    set_direction: SetDirection = field(default=SetDirection.forward)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpForEach":
        return cls(
            set_ref=reader.readRef(),
            set_direction=SetDirection(reader.read_u8()),
        )

    @override
    def source_line(self, inline: bool = False) -> str:
        return f"{keyword('for each (')} {self.set_ref} {keyword(')')}"