from .OpSetValue import COpSetValue
from .OpCode import COpCode

OPCODE_REGISTRY = {
    "set value": COpSetValue,
}

def getOpClassByName():
    pass