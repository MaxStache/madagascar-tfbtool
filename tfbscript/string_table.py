"""The three string tables at the head of every TFB script file."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tfbscript.binary import BinaryReader


@dataclass
class StringTableEntry:
    """One entry: a length-prefixed string plus 4 bytes of metadata.

    Entry strings are `::`-separated paths such as ``myactor::actor`` or
    ``myactor::user::value`` -- the first part is the name, the last part the
    type, and the middle part (if any) the category.
    """

    string: str
    metadata: bytes  # 4 bytes, usually zero

    @classmethod
    def read(cls, reader: "BinaryReader") -> "StringTableEntry":
        length = reader.read_u8()
        string = reader.read_string(length)
        metadata = reader.read_bytes(4)
        return cls(string, metadata)

    @property
    def name(self) -> str:
        return self.string.split("::")[0]

    @property
    def type(self) -> str:
        return self.string.split("::")[-1]

    @property
    def category(self) -> str | None:
        parts = self.string.split("::")
        return parts[-2] if len(parts) > 2 else None


@dataclass
class StringTable:
    """A u32 entry count followed by that many entries."""

    entries: list[StringTableEntry]

    @classmethod
    def read(cls, reader: "BinaryReader") -> "StringTable":
        count = reader.read_u32()
        return cls([StringTableEntry.read(reader) for _ in range(count)])

    def __len__(self) -> int:
        return len(self.entries)

    def get(self, index: int) -> StringTableEntry | None:
        if 0 <= index < len(self.entries):
            return self.entries[index]
        return None

    def all_with_type(self, type_name: str) -> list[StringTableEntry]:
        """All entries whose type (last ``::`` part) matches, e.g. ``behavior``."""
        return [e for e in self.entries if e.type == type_name]

    def all_with_category(self, category_name: str) -> list[StringTableEntry]:
        """All entries whose category (middle ``::`` part) matches, e.g. ``user``."""
        return [e for e in self.entries if e.category == category_name]
