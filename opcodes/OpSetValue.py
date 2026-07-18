from dataclasses import dataclass, field

from utils.binaryReader import PayloadBinaryReader
from .OpCode import COpCode

from TFBScriptRHS import TFBScriptRHS
from TFBScriptReference import TFBScriptReference

from utils.ansi_text import keyword, operator

@dataclass
class COpSetValue(COpCode):
    lhs: TFBScriptReference = field(default_factory=TFBScriptReference)
    rhs: TFBScriptRHS = field(default_factory=TFBScriptRHS)

    @classmethod
    def readPayload(cls, reader: PayloadBinaryReader, flags):
        lhs = reader.readRef()
        rhs = reader.readRHS()

        return cls(lhs=lhs, rhs=rhs, flags=flags)

    def toString(self):
        return f"{keyword('set')} {self.lhs} {operator('=')} {self.rhs};"