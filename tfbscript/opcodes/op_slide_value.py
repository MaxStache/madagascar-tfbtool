from dataclasses import dataclass, field

from tfbscript.ansi import func_call
from tfbscript.opcodes.base import Opcode, opcode
from typing import override
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference
from tfbscript.rhs import Rhs


@opcode("slide value")
@dataclass
class OpSlideValue(Opcode):
    lhs: Reference = field(default_factory=Reference)
    target_value: Rhs = field(default_factory=Rhs)
    interpolation_time: Rhs = field(default_factory=Rhs)

    ease_out: Reference = field(default_factory=Reference)
    ease_in: Reference = field(default_factory=Reference)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> Opcode:
        return cls(
            lhs=reader.readRef(),
            target_value=Rhs.read(reader, reader.global_refs, reader.local_refs),
            interpolation_time=Rhs.read(reader, reader.global_refs, reader.local_refs),
            ease_out=reader.readRef(),
            ease_in=reader.readRef(),
        )

    @override
    def source_line(self, inline: bool = False) -> str:
        return (
            str(self.lhs)
            + "."
            + func_call(
                "slide",
                f"to {str(self.target_value)}",
                f"over {str(self.interpolation_time)}",
                f"ease in {str(self.ease_out)}",
                f"ease out {str(self.ease_in)}",
            )
        )