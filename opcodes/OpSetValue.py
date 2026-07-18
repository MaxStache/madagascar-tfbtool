from dataclasses import dataclass
from .OpCode import COpCode

@dataclass
class COpSetValue(COpCode):
    lhs: str
    rhs: str

    @classmethod
    def readPayload(cls, reader, flags):

        return cls(lhs=lhs, rhs=rhs, flags=flags)