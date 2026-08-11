from dataclasses import dataclass, field
from typing import override

from tfbscript.ansi import func_call
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.opcodes.enums import CutsceneCommand
from tfbscript.payload import PayloadReader

@opcode("cut-scene")
@dataclass
class OpCutScene(Opcode):
    cutscene_command: CutsceneCommand = field(default=CutsceneCommand.Begin)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpCutScene":
        cutscene_cmd = CutsceneCommand(reader.read_u8())
        return cls(cutscene_command=cutscene_cmd)

    @override
    def source_line(self, inline: bool = False) -> str:
        return func_call("cutScene", str(self.cutscene_command))
