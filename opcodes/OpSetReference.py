from dataclasses import dataclass, field

from utils.binaryReader import PayloadBinaryReader
from .OpCode import COpCode

from TFBScriptReference import TFBScriptReference

from utils.ansi_text import keyword

@dataclass
class COpSetReference(COpCode):
    dest_ref: TFBScriptReference = field(default_factory=TFBScriptReference)
    src_ref: TFBScriptReference = field(default_factory=TFBScriptReference)

    @classmethod
    def readPayload(cls, reader: PayloadBinaryReader, flags):
        dest_ref = reader.readRef()
        src_ref = reader.readRef()

        return cls(dest_ref=dest_ref, src_ref=src_ref, flags=flags)

    def toString(self):
        return f"{keyword('set reference')} *{self.dest_ref} = {self.src_ref};"