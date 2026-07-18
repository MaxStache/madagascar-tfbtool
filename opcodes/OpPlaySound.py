from dataclasses import dataclass, field

from TFBScriptReference import TFBScriptReference
from utils.binaryReader import PayloadBinaryReader
from .OpCode import COpCode, InstructionFlags
from utils.ansi_text import method, parentheses

@dataclass
class COpPlaySound(COpCode):
    lhs: TFBScriptReference = field(default_factory=TFBScriptReference)

    @classmethod
    def readPayload(cls, reader: PayloadBinaryReader, flags: InstructionFlags):

        lhs = reader.readRef() # sound to play

        return cls(lhs=lhs)

    def toString(self):
        return f"{self.lhs}.{method('play')}{parentheses('()')};"