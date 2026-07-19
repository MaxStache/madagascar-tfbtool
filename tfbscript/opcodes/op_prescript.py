from dataclasses import dataclass

from tfbscript.opcodes.block import BlockOpcode


@dataclass
class OpPrescript(BlockOpcode):
    def block_name(self) -> str:
        return "PRESCRIPT"
