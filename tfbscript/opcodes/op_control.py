from dataclasses import dataclass, field

from tfbscript.ansi import keyword, method, parentheses
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.opcodes.enums import ControlRequirement
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("control")
@dataclass
class OpControl(Opcode):
    target: Reference = field(default_factory=Reference)
    readyness_requirement: ControlRequirement = field(default=ControlRequirement.Strict)

    @classmethod
    def parse_payload(cls, reader: PayloadReader) -> "OpControl":
        target = reader.readRef()

        # CLEANUP: this doesnt look too nice
        readyness_requirement = ControlRequirement.Strict
        if reader.size_remaining() > 0:
            if reader.read_u8() >= 1:
                readyness_requirement = ControlRequirement.Lenient
            else:
                readyness_requirement = ControlRequirement.Strict

        return cls(
            target=target,
            readyness_requirement=readyness_requirement
        )
    
    def source_line(self, inline: bool = False) -> str:
        return f"{keyword("control (")} {self.target} {keyword(")")} {method("requirement:")} {self.readyness_requirement}"
    
    def print_tree(self, indent: int = 0) -> None:
        print(f"{'    ' * indent}{self.source_line()}")
        for child in self.children:
            child.print_tree(indent + 1)
