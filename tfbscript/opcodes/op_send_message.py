from dataclasses import dataclass, field
from typing import override

from tfbscript.ansi import func_call
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference
from tfbscript.rhs import Rhs


@opcode("send message")
@dataclass
class OpSendMessage(Opcode):
    message_ref: Reference = field(default_factory=Reference)
    reciver_Ref: Reference = field(default_factory=Reference)
    unknown: int = field(default=0)
    value: Rhs = field(default_factory=Rhs)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpSendMessage":
        return cls(
            message_ref=reader.readRef(),
            reciver_Ref=reader.readRef(),
            unknown=reader.read_u8(),
            value=reader.readRHS(),
        )

    @override
    def source_line(self, inline: bool = False) -> str:
        return func_call(
            "sendMessage",
            str(self.message_ref),
            f"to: {self.reciver_Ref}",
            f"unknown: {self.unknown}",
            f"value: {self.value}",
        )
