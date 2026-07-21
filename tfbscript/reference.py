"""The 4-byte bit-packed variable reference used throughout opcode payloads."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from tfbscript.ansi import builtin, variable, variable_global
from tfbscript.string_table import StringTable, StringTableEntry

if TYPE_CHECKING:
    from tfbscript.binary import BinaryReader

# --- constants from FUN_00432f70 ------------------------------------------
LOCAL_BASE = 0x3FC0D  # index >= this (and < BUILTIN_BASE) => script-local
BUILTIN_BASE = 0x3FFFA  # index >= this => engine built-in object
NULL_REF = 0xFFFFFFFF

# index -> built-in name. Each FUN_00433140(kind) call walks backward through
# enclosing scopes for the nearest one whose OWN category getter (vtbl+0x2c)
# returns `kind` -- these are not fixed global sentinels, they're dynamically
# resolved relative to where the reference appears (same mechanism as `self`).
BUILTINS = {
    0x3FFFF: "self",  # FUN_00433140(2)    -- confirmed: nearest enclosing actor scope
    0x3FFFE: "[~controlled]",  # FUN_00433140(0)     -- provisional builtin(0)
    0x3FFFD: "[~each]",  # FUN_00433140(0x65)  -- confirmed: nearest enclosing `for each`'s
    #   current item (for_each's own category getter, FUN_0043cc70,
    #   returns 0x65; seen in the wild assigned out of a for-each body)
    0x3FFFC: "[~subset]",  # FUN_00433140(3)     -- provisional builtin(3)
    0x3FFFB: "[~found]",  # FUN_00436e30()      -- provisional
    0x3FFFA: "[~found_variable]",  # FUN_00433140(6)     -- provisional builtin(6)
}


@dataclass
class Reference:
    raw: int = 0x00  # the 32-bit little-endian value R
    index: int = 0  # R >> 14
    member: int = 0  # (R >> 8) & 0x3F  -- field within the target
    scope: int = 0  # (R >> 6) & 3
    sub: int = 0  # R & 0x3F
    kind: str = "null"  # 'null' | 'builtin' | 'global' | 'local'
    slot: int | None = None  # table index used for the lookup (None for null/builtin)
    name: str = "<null>"  # resolved name (or descriptive placeholder)
    entry: StringTableEntry | None = None  # resolved entry (None for null/builtin)

    @classmethod
    def read(
        cls,
        reader: "BinaryReader",
        global_refs: StringTable,
        local_refs: StringTable,
    ) -> "Reference":
        """Parse a 4-byte TFB-Script variable reference.

        Args:
            reader: BinaryReader positioned at the reference.
            global_refs: the script's 2nd string table (globals) for name resolution.
            local_refs: the script's 3rd string table (locals) for name resolution.
        Returns:
            A Reference with the decoded bit-fields and a resolved `name`.
        """
        if reader.size_remaining() < 4:
            raise ValueError("a reference is 4 bytes")

        raw = reader.read_u32()
        fields = dict(
            raw=raw,
            index=raw >> 14,
            member=(raw >> 8) & 0x3F,
            scope=(raw >> 6) & 3,
            sub=raw & 0x3F,
        )
        index = fields["index"]

        if raw == NULL_REF:
            return cls(**fields, kind="null", slot=None, name="<null>", entry=None)

        if index >= BUILTIN_BASE:
            name = BUILTINS.get(index, f"builtin@{index:#x}")
            return cls(**fields, kind="builtin", slot=None, name=name, entry=None)

        if index < LOCAL_BASE:
            entry = global_refs.get(index)
            name = entry.string if entry is not None else f"unk_global#{index}"
            return cls(**fields, kind="global", slot=index, name=name, entry=entry)

        slot = index - LOCAL_BASE
        entry = local_refs.get(slot)
        name = entry.string if entry is not None else f"local#{slot}"
        return cls(**fields, kind="local", slot=slot, name=name, entry=entry)

    @override
    def __str__(self) -> str:
        if self.kind == "null":
            return "<null>"

        if self.kind == "global":
            s = variable_global(f"global[ {self.name.split('::')[0]} ]")
        elif self.kind == "local" and self.entry is not None:
            s = variable(self.entry.name)
        elif self.kind == "builtin":
            s = builtin(self.name)
        else:
            s = self.name

        if self.member:
            s += f".field[{self.member:#04x}]"
        if self.sub:
            s += f".sub[{self.sub:#04x}]"
        if self.scope:
            s += f"@{self.scope}"  # set index for example
        return s
