from dataclasses import dataclass, field
from typing import override

from tfbscript.ansi import func_call
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.opcodes.enums import AnimationMapping
from tfbscript.payload import PayloadReader
from tfbscript.rhs import Rhs


@opcode(
    "turn to",
    "Turns to either an actor reference or an angle while playing an animation.",
)
@dataclass
class OpTurnTo(Opcode):
    rhs: Rhs = field(default_factory=Rhs)  # angle or actor reference
    animation: AnimationMapping = field(default=AnimationMapping.ambient)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpTurnTo":
        return cls(rhs=reader.readRHS(), animation=AnimationMapping(reader.read_u8()))

    @override
    def source_line(self, inline: bool = False) -> str:
        return func_call("turnTo", str(self.rhs), f"animation: {self.animation}")
