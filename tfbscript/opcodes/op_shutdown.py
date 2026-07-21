from dataclasses import dataclass
from typing import override

from tfbscript.opcodes.block import BlockOpcode


@dataclass
class OpShutdown(BlockOpcode):
    @override
    def block_name(self) -> str:
        return "SHUTDOWN"
