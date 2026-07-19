from dataclasses import dataclass

from tfbscript.ansi import keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader


@opcode("if/else")
@dataclass
class OpIfElse(Opcode):
    # No payload of its own. The first child is the condition opcode; the
    # condition's own children are the "then" branch, and any remaining
    # children of the if/else are the "else" branch.

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpIfElse":
        return cls()

    def print_tree(self, indent: int = 0) -> None:
        if not self.children:
            return

        pad = "    " * indent
        condition = self.children[0]

        print(f"{pad}{keyword('if (')} {condition.source_line(inline=True)} {keyword(') {')}")
        for then_child in condition.children:
            then_child.print_tree(indent + 1)

        print(pad + keyword("} else {"))
        for else_child in self.children[1:]:
            else_child.print_tree(indent + 1)

        print(pad + keyword("}"))
