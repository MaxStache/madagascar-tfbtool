from dataclasses import dataclass, field

from tfbscript.ansi import Color, color_text, comparison, func_call, parentheses, variable
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.opcodes.enums import RelOp
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference
from tfbscript.rhs import Rhs


@opcode("find subset")
@dataclass
class OpFindSubset(Opcode):
    """Filters a set by a condition; yields the subset of items that match."""

    set_ref: Reference = field(default_factory=Reference)
    rel_op: RelOp = RelOp.Eq
    rhs: Rhs = field(default_factory=Rhs)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpFindSubset":
        set_ref = reader.readRef()
        rel_op = RelOp(reader.read_u8())
        rhs = reader.readRHS()
        return cls(set_ref=set_ref, rel_op=rel_op, rhs=rhs)

    def source_line(self, inline: bool = False) -> str:
        # Rendered as: set.filter((val) => { val <op> rhs })
        val = variable("val")
        arrow = color_text("=>", Color.INLINE_FUNC_OP)
        lambda_src = (
            f"{parentheses('(')}{val}{parentheses(')')} {arrow} "
            f"{parentheses('{')} {val} {comparison(self.rel_op.symbol())} {self.rhs} {parentheses('}')}"
        )
        return f"{self.set_ref}.{func_call('filter', lambda_src)}"
