from dataclasses import dataclass, field

from tfbscript.ansi import func_call, method, parentheses
from tfbscript.opcodes.base import Opcode, opcode
from typing import override
from tfbscript.opcodes.enums import AnimationMapping
from tfbscript.payload import PayloadReader


@opcode("play animation")
@dataclass
class OpPlayAnimation(Opcode):
    animation: AnimationMapping = field(default=AnimationMapping.ambient)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpPlayAnimation":
        return cls(animation=AnimationMapping(reader.read_u8()))

    @override
    def source_line(self, inline: bool = False) -> str:
        if self.children:
            return f"when {method("playAnimation")}{parentheses('(')}{self.animation!s}{parentheses(')')} is done playing, do:"
        return func_call("playAnimation", str(self.animation))