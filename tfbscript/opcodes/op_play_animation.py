from dataclasses import dataclass, field

from tfbscript.ansi import func_call, method, number, parentheses
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader


@opcode("play animation")
@dataclass
class OpPlayAnimation(Opcode):
    animation_idx: int = field(default=0)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpPlayAnimation":
        return cls(animation_idx=reader.read_u8())

    def source_line(self, inline: bool = False) -> str:
        if self.children:
            return f"when {method("playAnimation")}{parentheses('(')}{number(self.animation_idx)}{parentheses(')')} is done playing, do:"
        return func_call("playAnimation", number(self.animation_idx))
