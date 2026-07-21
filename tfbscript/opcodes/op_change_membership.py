from dataclasses import dataclass, field

from tfbscript.ansi import method, parentheses
from tfbscript.opcodes.base import Opcode, opcode
from typing import override
from tfbscript.opcodes.enums import MembershipCombiner
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("change membership")
@dataclass
class OpChangeMembership(Opcode):
    ref: Reference = field(default_factory=Reference)
    membershipCombiner: MembershipCombiner = field(default=MembershipCombiner.add)
    ref2: Reference = field(default_factory=Reference)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpChangeMembership":
        ref = reader.readRef()
        membershipCombiner = MembershipCombiner(reader.read_u8())
        ref2 = reader.readRef()
        return cls(ref=ref, membershipCombiner=membershipCombiner, ref2=ref2)

    @override
    def source_line(self, inline: bool = False) -> str:
        return f"{self.ref}.{method(self.membershipCombiner.symbol())}{parentheses('(')}{self.ref2}{parentheses(')')};"
