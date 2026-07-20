from dataclasses import dataclass, field

from tfbscript.ansi import flow_control, keyword
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("check reference")
@dataclass
class OpCheckReference(Opcode):
    ref1: Reference = field(default_factory=Reference)
    ref2: Reference = field(default_factory=Reference)


    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpCheckReference":
        ref1 = reader.readRef()
        ref2 = reader.readRef()

        return cls(ref1=ref1, ref2=ref2)

    def source_line(self, inline: bool = False) -> str:
        condition = f"*{self.ref1} is reference to {self.ref2}"
        if inline:
            return condition

        return f"{keyword('check reference (')} {condition} {keyword(') {')}"

    def print_tree(self, indent: int = 0) -> None:
        super().print_tree(indent)
        pad = "    " * indent
        print(f"{pad}    {keyword('flow ')}{flow_control(self.flags.flow_control_str())}")
        print(f"{pad}{keyword('}')}")
