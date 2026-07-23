from dataclasses import dataclass, field
import sys
from typing import override

from tfbscript.ansi import keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("spawn actor")
@dataclass
class OpSpawnActor(Opcode):

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpSpawnActor":
        print(
            reader.readRef(),
            file=sys.stderr,
        )
        print(
            reader.readRef(),
            file=sys.stderr,
        )
        print(
            reader.readRHS(),
            file=sys.stderr,
        )
        return cls()

    @override
    def source_line(self, inline: bool = False) -> str:
        return f"{keyword('spawn actor')};"
