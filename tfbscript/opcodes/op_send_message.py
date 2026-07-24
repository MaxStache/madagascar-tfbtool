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
    value: Rhs = field(default_factory=Rhs)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpSendMessage":
        message_ref = reader.readRef()
        reciver_ref = reader.readRef()
        _relop = reader.skip(1)
        # Send Message uses same payload parser as check message
        # Relop is unused here in send and discarded

        value = reader.readRHS()
        return cls(
            message_ref=message_ref,
            reciver_Ref=reciver_ref,
            value=value,
        )

    @override
    def source_line(self, inline: bool = False) -> str:
        return func_call(
            "sendMessage",
            str(self.message_ref),
            f"to: {self.reciver_Ref}",
            f"value: {self.value}",
        )
