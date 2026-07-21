from dataclasses import dataclass, field

from tfbscript.ansi import func_call, number
from tfbscript.opcodes.base import Opcode, opcode
from typing import override
from tfbscript.payload import PayloadReader
from tfbscript.rhs import Rhs


@opcode("turn to", "Turns to either an actor reference or an angle while playing an animation.")
@dataclass
class OpTurnTo(Opcode):
    rhs: Rhs = field(default_factory=Rhs) # angle or actor reference
    animation_idx: int = 0 # index of animation to play while turning

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpTurnTo":
        return cls(rhs=reader.readRHS(), animation_idx=reader.read_u8())

    @override
    def source_line(self, inline: bool = False) -> str:
        return func_call("turnTo", str(self.rhs), f"animation: {number(self.animation_idx)}")
