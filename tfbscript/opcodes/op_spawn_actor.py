from dataclasses import dataclass, field
from typing import override

from tfbscript.ansi import keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference
from tfbscript.rhs import Rhs


@opcode("spawn actor")
@dataclass
class OpSpawnActor(Opcode):
    clone_ref: Reference = field(default_factory=Reference)
    at_ref: Reference = field(default_factory=Reference)
    facing_rhs: Rhs = field(default_factory=Rhs)
    remaining: int | None = None

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpSpawnActor":
        clone_ref = reader.readRef()
        at_ref = reader.readRef()
        facing_rhs = reader.readRHS()   

        if reader.size_remaining() > 0:
            return cls(clone_ref=clone_ref, at_ref=at_ref, facing_rhs=facing_rhs, remaining=reader.read_u8())
        return cls(clone_ref=clone_ref, at_ref=at_ref, facing_rhs=facing_rhs)

    @override
    def source_line(self, inline: bool = False) -> str:
        if self.remaining is not None:
            return f"{keyword(f'spawn actor ({self.clone_ref}, at: {self.at_ref}, facing: {self.facing_rhs}, unknown: {self.remaining})')};"
        else:
            return f"{keyword(f'spawn actor ({self.clone_ref}, at: {self.at_ref}, facing: {self.facing_rhs})')};"