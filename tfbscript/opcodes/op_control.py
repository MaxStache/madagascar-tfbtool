from dataclasses import dataclass, field
from typing import override

from tfbscript.ansi import keyword, method
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

        # CLEANUP: this doesnt look too nice
        script_control = ControlRequirement.Allow
        if reader.size_remaining() > 0:
            script_control = ControlRequirement(reader.read_u8())

        return cls(target=target, script_control=script_control)

    @override
    def source_line(self, inline: bool = False) -> str:
        return f"{keyword('control (')} {self.target}, {self.script_control} {keyword(')')}"
