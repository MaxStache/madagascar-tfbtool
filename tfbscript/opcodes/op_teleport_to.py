from dataclasses import dataclass, field

from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.opcodes.enums import SetDirection
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference
from tfbscript.rhs import Rhs

# TODO: TODO: TODO: IMPLEMENT

@opcode("teleport to")
@dataclass
class OpTeleportTo(Opcode):
    target_ref: Reference = field(default_factory=Reference)
    set_direction: SetDirection = field(default=SetDirection.forward)
    facing: Rhs = field(default_factory=Rhs)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpTeleportTo":
        target_ref= reader.readRef()
        set_direction = SetDirection(reader.read_u8())
        facing = reader.readRHS()

        print(reader.read_bytes(reader.size_remaining()))

        return cls(
            target_ref=target_ref,
            set_direction=set_direction,
            facing=facing,
        )

    def source_line(self, inline: bool = False) -> str:
        return "TELEPORT TO"
