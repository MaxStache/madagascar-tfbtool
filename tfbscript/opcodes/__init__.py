"""Opcode implementations, one module per opcode.

Importing this package registers every implemented opcode in OPCODE_REGISTRY
(via the @opcode decorator); unimplemented opcodes fall back to the generic
Opcode class, which keeps the raw payload.
"""

from tfbscript.opcodes.base import OPCODE_REGISTRY, InstructionFlags, Opcode, ParserContext
from tfbscript.opcodes.block import BlockOpcode
from tfbscript.opcodes.enums import RelOp
from tfbscript.opcodes.op_behavior_implementation import OpBehaviorImplementation
from tfbscript.opcodes.op_check_value import OpCheckValue
from tfbscript.opcodes.op_control import OpControl
from tfbscript.opcodes.op_create_variable import OpCreateVariable
from tfbscript.opcodes.op_dec_value import OpDecValue
from tfbscript.opcodes.op_find_subset import OpFindSubset
from tfbscript.opcodes.op_if_else import OpIfElse
from tfbscript.opcodes.op_inc_value import OpIncValue
from tfbscript.opcodes.op_play_sound import OpPlaySound
from tfbscript.opcodes.op_stop_sound import OpStopSound
from tfbscript.opcodes.op_prescript import OpPrescript
from tfbscript.opcodes.op_print import OpPrint
from tfbscript.opcodes.op_remove import OpRemove
from tfbscript.opcodes.op_set_behavior import OpSetBehavior
from tfbscript.opcodes.op_set_reference import OpSetReference
from tfbscript.opcodes.op_set_value import OpSetValue
from tfbscript.opcodes.op_shutdown import OpShutdown
from tfbscript.opcodes.op_slide_value import OpSlideValue
from tfbscript.opcodes.op_startup import OpStartup
from tfbscript.opcodes.op_comment import OpComment
from tfbscript.opcodes.op_teleport_to import OpTeleportTo
from tfbscript.opcodes.op_run_as_player import OpRunAsPlayer
from tfbscript.opcodes.op_cut_scene import OpCutScene
from tfbscript.opcodes.op_displace import OpDisplace
from tfbscript.opcodes.op_reset import OpReset
from tfbscript.opcodes.op_play_animation import OpPlayAnimation
from tfbscript.opcodes.op_check_reference import OpCheckReference
from tfbscript.opcodes.op_turn_to import OpTurnTo

__all__ = [
    "OPCODE_REGISTRY",
    "BlockOpcode",
    "InstructionFlags",
    "Opcode",
    "ParserContext",
    "RelOp",
    "OpBehaviorImplementation",
    "OpCheckValue",
    "OpControl",
    "OpCreateVariable",
    "OpDecValue",
    "OpFindSubset",
    "OpIfElse",
    "OpIncValue",
    "OpPlaySound",
    "OpStopSound",
    "OpPrescript",
    "OpPrint",
    "OpRemove",
    "OpSetBehavior",
    "OpSetReference",
    "OpSetValue",
    "OpShutdown",
    "OpSlideValue",
    "OpStartup",
    "OpComment",
    "OpTeleportTo",
    "OpRunAsPlayer",
    "OpCutScene",
    "OpDisplace",
    "OpReset",
    "OpPlayAnimation",
    "OpCheckReference",
    "OpTurnTo",
]
