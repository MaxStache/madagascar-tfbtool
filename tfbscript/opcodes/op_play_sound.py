from dataclasses import dataclass, field

from tfbscript.ansi import method, parentheses
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("play sound")
@dataclass
class OpPlaySound(Opcode):
    sound: Reference = field(default_factory=Reference)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpPlaySound":
        return cls(sound=reader.read_reference())

    def source_line(self, inline: bool = False) -> str:
        return f"{self.sound}.{method('play')}{parentheses('()')};"
