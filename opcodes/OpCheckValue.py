from dataclasses import dataclass, field

from opcodes.enums.RelOp import ERelOp
from utils.binaryReader import PayloadBinaryReader
from .OpCode import COpCode

from TFBScriptRHS import TFBScriptRHS
from TFBScriptReference import TFBScriptReference

from utils.ansi_text import keyword, comparison, flow_control


@dataclass
class COpCheckValue(COpCode):
    lhs: TFBScriptReference = field(default_factory=TFBScriptReference)
    rel_op: ERelOp = field(default=ERelOp.Eq)
    rhs: TFBScriptRHS = field(default_factory=TFBScriptRHS)

    @classmethod
    def readPayload(cls, reader: PayloadBinaryReader, flags):
        lhs = reader.readRef()
        rel_op = ERelOp(reader.readUint8())
        rhs = reader.readRHS()

        return cls(lhs=lhs, rel_op=rel_op, rhs=rhs, flags=flags)

    def print(self, indent=0):
        super().print(indent)
        indent_str = " " * 4 * indent
        child_indent_str = " " * 4 * (indent + 1)

        print(f"{child_indent_str}{keyword('flow ')}{flow_control(self.flags.flowControlToString())}")
        print(f"{indent_str}{keyword('}')}")

    def toString(self):
        return f"{keyword('if (')} {self.lhs} {comparison(self.rel_op.symbol())} {self.rhs} {keyword(') {')}"
