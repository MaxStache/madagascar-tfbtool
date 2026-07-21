from dataclasses import dataclass, field

from tfbscript.ansi import func_call
from tfbscript.opcodes.base import Opcode, opcode
from typing import override
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("run as player")
@dataclass
class OpRunAsPlayer(Opcode):
    actor_ref: Reference = field(default_factory=Reference)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpRunAsPlayer":
        return cls(actor_ref=reader.readRef())

    @override
    def source_line(self, inline: bool = False) -> str:
        return func_call("runAsPlayer", str(self.actor_ref))
