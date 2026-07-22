from dataclasses import dataclass, field

from tfbscript.ansi import keyword
from tfbscript.opcodes.base import Opcode, opcode
from typing import override
from tfbscript.opcodes.enums import RelOp
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference
from tfbscript.rhs import Rhs


@opcode("check message")
@dataclass
class OpCheckMessage(Opcode):
    message_ref: Reference = field(default_factory=Reference)

    sender_ref: Reference = field(default_factory=Reference)
    rel_op: RelOp = field(default=RelOp.Eq)
    value: Rhs = field(default_factory=Rhs)

    _is_extended: bool = field(
        default=False
    )  # has sender_ref, rel_op, value determined if payload > 4

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpCheckMessage":
        message_ref = reader.readRef()

        # Ref: 4b
        # RelOp: 1b
        # Rhs: min. 5b
        if reader.size_remaining() >= 4 + 1 + 5:
            sender_ref = reader.readRef()

            rel_op = RelOp(reader.read_u8())
            value = reader.readRHS()

            return cls(
                message_ref=message_ref,
                sender_ref=sender_ref,
                rel_op=rel_op,
                value=value,
                _is_extended=True,
            )
        
        return cls(
            message_ref=message_ref,
            _is_extended=False,
        )

    @override
    def source_line(self, inline: bool = False) -> str:
        if self._is_extended:
            condition = f"value {self.rel_op} {self.value}"
            return f"{keyword('check message (')} {self.message_ref}, sent by: {self.sender_ref}, where: {condition} {keyword(')')}"
        else:
            return f"{keyword('check message (')} {self.message_ref} {keyword(')')}"