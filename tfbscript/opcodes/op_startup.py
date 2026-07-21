from dataclasses import dataclass
from typing import override

from tfbscript.opcodes.block import BlockOpcode


@dataclass
class OpStartup(BlockOpcode):
    @override
    def block_name(self) -> str:
        return "STARTUP"
