from dataclasses import dataclass, field

from tfbscript.opcodes.base import Opcode, opcode
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
    def parse_payload(cls, reader: PayloadReader) -> Opcode:
        return cls(
            lhs=reader.read_reference(),
            target_value=Rhs.read(reader, reader.global_refs, reader.local_refs),
            interpolation_time=Rhs.read(reader, reader.global_refs, reader.local_refs),
            ease_out=reader.read_reference(),
            ease_in=reader.read_reference(),
        )
    
    def toString(self) -> str:
        return f"{self.lhs} = slide({self.target_value}, {self.interpolation_time}, {self.ease_out}, {self.ease_in})"