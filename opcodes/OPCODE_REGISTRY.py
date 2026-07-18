from .OpSetValue import COpSetValue
from .OpIfElse import COpIfElse
from .OpCreateVariable import COpCreateVariable
from .OpCheckValue import COpCheckValue
from .OpIncValue import COpIncValue
from .OpSetReference import COpSetReference
from .OpRemove import COpRemove
from .OpPlaySound import COpPlaySound

OPCODE_REGISTRY = {
    "set value": COpSetValue,
    "check value": COpCheckValue,
    "inc value": COpIncValue,
    "set reference": COpSetReference,
    "remove": COpRemove,
    "play sound": COpPlaySound,
    #"if/else": COpIfElse,
    "create variable": COpCreateVariable,
}
