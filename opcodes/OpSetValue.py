from dataclasses import dataclass
from .OpCode import OpCode

@dataclass
class OpSetValue(OpCode):
    lhs: str
    rhs: str