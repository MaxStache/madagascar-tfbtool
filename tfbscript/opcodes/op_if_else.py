from dataclasses import dataclass
from typing import override

from tfbscript.ansi import flow_control, keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader


@opcode("if/else")
@dataclass
class OpIfElse(Opcode):
    # No payload of its own. The first child is the condition opcode; the
    # condition's own children are the "then" branch, and any remaining
    # children of the if/else are the "else" branch.

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpIfElse":
        return cls()

    @override
    def print_tree(self, indent: int = 0, chained: bool = False) -> None:
        if not self.children:
            return

        pad = "    " * indent
        condition = self.children[0]

        keyword_str = "} else if (" if chained else "if ("

        print(
            f"{pad}{keyword(keyword_str)} {condition.source_line(inline=True)} {keyword(') {')}"
        )

        for then_child in condition.children:
            then_child.print_tree(indent + 1)

        print(f"{'    ' * (indent + 1)}{keyword('flow ')}{flow_control(self.flags.flow_control_str())}")

        else_children = self.children[1:]

        # None
        if not else_children:
            print(pad + keyword("}"))
        # ELSE IF
        elif len(else_children) == 1 and isinstance(else_children[0], OpIfElse):
            fist_child = else_children[0]
            fist_child.print_tree(indent, chained=True) # type: ignore

            print(f"{'    ' * (indent + 1)}{keyword('flow ')}{flow_control(self.flags.flow_control_str())}")
        # ELSE
        else:
            print(pad + keyword("} else {"))
            for else_child in else_children:
                else_child.print_tree(indent + 1)

            print(f"{'    ' * (indent + 1)}{keyword('flow ')}{flow_control(self.flags.flow_control_str())}")

            print(pad + keyword("}"))
