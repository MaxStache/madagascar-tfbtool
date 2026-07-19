from dataclasses import dataclass, field

from tfbscript.ansi import func_call, method, parentheses
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference

# TODO: TODO: TODO: Verify

@opcode("cut-scene")
@dataclass
class OpCutScene(Opcode):
    cutscene_command: Reference = field(default_factory=Reference)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpCutScene":
        return cls(cutscene_command=reader.readRef())

    def source_line(self, inline: bool = False) -> str:
        return func_call("cutScene", str(self.cutscene_command))
