from dataclasses import dataclass

from tfbscript.opcodes.base import Opcode, opcode


@opcode("control")
@dataclass
class OpControl(Opcode):
    """Payload layout not reverse engineered yet; parsed as the generic fallback."""
