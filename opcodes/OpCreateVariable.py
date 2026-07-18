from dataclasses import dataclass, field

from TFBScriptReference import TFBScriptReference
from utils.binaryReader import PayloadBinaryReader
from .OpCode import COpCode, InstructionFlags
from utils.ansi_text import keyword, type_

@dataclass
class COpCreateVariable(COpCode):
    variable: TFBScriptReference = field(default_factory=TFBScriptReference)

    @classmethod
    def readPayload(cls, reader: PayloadBinaryReader, flags: InstructionFlags):

        variable = reader.readRef()

        return cls(variable=variable)

    def toString(self):
        varType = self.variable.entry.getType() if self.variable.entry else "unknown"
        return f"{keyword('var')} {self.variable} : {type_(varType)};"