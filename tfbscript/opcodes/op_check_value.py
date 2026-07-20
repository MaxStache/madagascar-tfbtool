from dataclasses import dataclass, field

from tfbscript.ansi import comparison, flow_control, keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.opcodes.enums import RelOp
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference
from tfbscript.rhs import Rhs


@opcode("check value")
@dataclass
class OpCheckValue(Opcode):
    lhs: Reference = field(default_factory=Reference)
    rel_op: RelOp = RelOp.Eq
    rhs: Rhs = field(default_factory=Rhs)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpCheckValue":
        lhs = reader.readRef()
        rel_op = RelOp(reader.read_u8())
        rhs = reader.readRHS()
        return cls(lhs=lhs, rel_op=rel_op, rhs=rhs)

    def source_line(self, inline: bool = False) -> str:
        condition = f"{self.lhs} {comparison(self.rel_op.symbol())} {self.rhs}"
        if inline:
            return condition

        return f"{keyword('check value (')} {condition} {keyword(') {')}"

    def print_tree(self, indent: int = 0) -> None:
        super().print_tree(indent)
        pad = "    " * indent
        flow = self.flags.flow_control_str()
        print(f"{pad}    {keyword('flow ')}{flow_control(flow)}")
        print(f"{pad}{keyword('}')}")
