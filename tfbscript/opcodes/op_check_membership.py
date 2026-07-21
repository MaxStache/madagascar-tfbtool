from dataclasses import dataclass, field
from typing import override

from tfbscript.ansi import comparison, keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.opcodes.enums import MembershipTest
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("check membership")
@dataclass
class OpCheckMembership(Opcode):
    ref1: Reference = field(default_factory=Reference)
    membershipTest: MembershipTest = MembershipTest.includes
    ref2: Reference = field(default_factory=Reference)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpCheckMembership":
        ref1 = reader.readRef()
        membershipTest = MembershipTest(reader.read_u8())
        ref2 = reader.readRef()
        return cls(ref1=ref1, membershipTest=membershipTest, ref2=ref2)

    @override
    def source_line(self, inline: bool = False) -> str:
        condition = f"{self.ref1} {comparison(self.membershipTest.symbol())} {self.ref2}"
        if inline:
            return condition

        return f"{keyword('check membership (')} {condition} {keyword(')')}"