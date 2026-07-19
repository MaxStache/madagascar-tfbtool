from dataclasses import dataclass

from tfbscript.opcodes.block import BlockOpcode


@dataclass
class OpShutdown(BlockOpcode):
    def block_name(self) -> str:
        return "SHUTDOWN"
