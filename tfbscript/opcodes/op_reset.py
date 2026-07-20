from dataclasses import dataclass, field

from tfbscript.ansi import method, parentheses
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("reset")
@dataclass
class OpReset(Opcode):
    target: Reference = field(default_factory=Reference)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpReset":
        return cls(target=reader.readRef())

    def source_line(self, inline: bool = False) -> str:
        return f"{self.target}.{method('reset')}{parentheses('()')};"
