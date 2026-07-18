from dataclasses import dataclass
from .OpCode import COpCode

@dataclass
class COpIfElse(COpCode):
    def __init__(self):
        raise NotImplementedError("COpIfElse is not implemented yet")