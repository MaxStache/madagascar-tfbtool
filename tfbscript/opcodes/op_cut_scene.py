from dataclasses import dataclass, field

from tfbscript.ansi import func_call
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.opcodes.enums import CutsceneCommand
from tfbscript.payload import PayloadReader

# TODO: TODO: TODO: Verify

@opcode("cut-scene")
@dataclass
class OpCutScene(Opcode):
    cutscene_command: CutsceneCommand = field(default=CutsceneCommand.Pause)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpCutScene":
        return cls(cutscene_command=CutsceneCommand(reader.read_u8()))

    def source_line(self, inline: bool = False) -> str:
        return func_call("cutScene", str(self.cutscene_command))
