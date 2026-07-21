from dataclasses import dataclass, field

from tfbscript.ansi import func_call
from tfbscript.opcodes.base import Opcode, opcode
from typing import override
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("set behavior")
@dataclass
class OpSetBehavior(Opcode):
    behavior: Reference = field(default_factory=Reference)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpSetBehavior":
        return cls(behavior=reader.readRef())

    @override
    def source_line(self, inline: bool = False) -> str:
        return func_call("setBehavior", str(self.behavior))
