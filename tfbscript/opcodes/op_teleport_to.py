from dataclasses import dataclass, field

from tfbscript.ansi import operator
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference

# TODO: TODO: TODO: IMPLEMENT

@opcode("teleport to")
@dataclass
class OpTeleportTo(Opcode):
    target_ref: Reference = field(default_factory=Reference)
    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpTeleportTo":
        return cls()

    def source_line(self, inline: bool = False) -> str:
        return ""
