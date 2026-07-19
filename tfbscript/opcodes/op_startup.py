from dataclasses import dataclass

from tfbscript.opcodes.block import BlockOpcode


@dataclass
class OpStartup(BlockOpcode):
    def block_name(self) -> str:
        return "STARTUP"
