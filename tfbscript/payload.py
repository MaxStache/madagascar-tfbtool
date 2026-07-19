"""Reader for opcode payloads, with access to the script's reference tables."""

from tfbscript.binary import BinaryReader
from tfbscript.reference import Reference
from tfbscript.rhs import Rhs
from tfbscript.string_table import StringTable


class PayloadReader(BinaryReader):
    """A BinaryReader over one opcode payload.

    Also carries the script's global/local reference tables so payload parsers
    can read References and RHS operands without threading the tables through.
    """

    def __init__(
        self,
        data: bytes,
        global_refs: StringTable,
        local_refs: StringTable,
        little_endian: bool = True,
    ):
        super().__init__(data, little_endian)
        self.global_refs = global_refs
        self.local_refs = local_refs

    def readRef(self) -> Reference:
        """Read a 4-byte TFB-Script variable reference."""
        return Reference.read(self, self.global_refs, self.local_refs)

    def readRHS(self) -> Rhs:
        """Read a 5-11 byte TFB-Script RHS operand."""
        return Rhs.read(self, self.global_refs, self.local_refs)
