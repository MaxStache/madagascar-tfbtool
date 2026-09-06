from dataclasses import dataclass, field
from typing import Any, BinaryIO, override

from tfbscript.ansi import keyword
from tfbscript.binary import write_u8
from tfbscript.opcodes.base import Opcode, opcode
from tfbscript.opcodes.enums import ControlRequirement
from tfbscript.payload import PayloadReader
from tfbscript.reference import Reference


@opcode("control")
@dataclass
class OpControl(Opcode):
    target: Reference = field(default_factory=Reference)
    script_control: ControlRequirement = field(default=ControlRequirement.Allow)

    @classmethod
    @override
    def parse_payload(cls, reader: PayloadReader) -> "OpControl":
        target = reader.readRef()

        script_control = ControlRequirement.Allow

        if target.get_final_type() == "actor":
            script_control = ControlRequirement(reader.read_u8())

        return cls(target=target, script_control=script_control)

    @override
    def source_line(self, inline: bool = False) -> str:
        return f"{keyword('control (')} {self.target}, {self.script_control} {keyword(')')}"

    @override
    def write_payload(self, f: BinaryIO) -> None:
        self.target.write(f)
        if self.target.get_final_type() == "actor":
            write_u8(f, self.script_control)

    @override
    def editor_repr(self) -> dict[str, Any]:
        return {
            "hasBody": True,
            "fields": [
                {
                    "type": "op-label",
                    "value": "control",
                },
                {
                    "type": "ref",
                    "name": "target",
                    "ref": self.target,
                },
                {
                    "type": "op-label",
                    "value": "script control: ",
                },
                {
                    "type": "enum",
                    "name": "script_control",
                    "entry": self.script_control,
                },
            ],
        }
