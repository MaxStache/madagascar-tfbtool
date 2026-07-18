"""
BASED ON REASEARCH AND REVERSE ENGENEERING BY CLAUDE, THIS FILE IS PARTIALLY AI GENERATED!
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from TFBStringTable import TFBStringTable_Entry

if TYPE_CHECKING:
    from TFBStringTable import TFBStringTable
    from utils.binaryReader import BinaryReader

from utils.ansi_text import variable_global, variable, builtin

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


def _entry_name(table: TFBStringTable, idx: int) -> TFBStringTable_Entry | None:
    if idx < 0 or idx >= len(table.entries):
        return None

    e = table.entries[idx]

    return e


@dataclass
class TFBScriptReference:
    raw: int = 0x00  # the 32-bit little-endian value R
    index: int = 0  # R >> 14
    member: int = 0  # (R >> 8) & 0x3F  -- field within the target
    scope: int = 0  # (R >> 6) & 3
    sub: int = 0  # R & 0x3F
    kind: str = "null"  # 'null' | 'builtin' | 'global' | 'local'
    slot: Optional[int] = None  # table index used for the lookup (None for null/builtin)
    name: str = "<null>"  # resolved name (or descriptive placeholder)

    entry: Optional["TFBStringTable_Entry"] = None  # resolved entry (None for null/builtin)

    def __str__(self) -> str:
        if self.kind == "null":
            return "<null>"

        s = ""
        if self.kind == "global":
            s = variable_global(f"global[ {self.name.split("::")[0]} ]")
        else:
            if self.kind == "local" and self.entry is not None:
                s = variable(self.entry.getName())
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

    @classmethod
    def read(
        cls, reader: BinaryReader, globalRefTable, localRefTable
    ) -> "TFBScriptReference":
        """Parse a 4-byte TFB-Script variable reference.
        Args:
            reader: BinaryReader
            globalRefTable: the script's 2rd string table (globals) for name resolution.
            localRefTable: the script's 3rd string table (locals) for name resolution.
        Returns:
            A Reference with the decoded bit-field and a resolved `name`.
        """
        if reader.sizeRemaining() < 4:
            raise ValueError("a reference is 4 bytes")

        R = reader.readUint32()
        index = R >> 14
        member = (R >> 8) & 0x3F
        scope = (R >> 6) & 3
        sub = R & 0x3F

        if R == NULL_REF:
            return cls(
                raw=R,
                index=index,
                member=member,
                scope=scope,
                sub=sub,
                kind="null",
                slot=None,
                name="<null>",
                entry=None,
            )

        if index >= BUILTIN_BASE:
            return cls(
                raw=R,
                index=index,
                member=member,
                scope=scope,
                sub=sub,
                kind="builtin",
                slot=None,
                name=BUILTINS.get(index, f"builtin@{index:#x}"),
                entry=None,
            )

        if index < LOCAL_BASE:
            entry = _entry_name(globalRefTable, index)
            name = entry.string if entry is not None else None
            return cls(
                raw=R,
                index=index,
                member=member,
                scope=scope,
                sub=sub,
                kind="global",
                slot=index,
                name=name if name is not None else f"unk_global#{index}",
                entry=entry,
            )

        slot = index - LOCAL_BASE
        entry = _entry_name(localRefTable, slot)
        name = entry.string if entry is not None else None
        return cls(
            raw=R,
            index=index,
            member=member,
            scope=scope,
            sub=sub,
            kind="local",
            slot=slot,
            name=name if name is not None else f"local#{slot}",
            entry=entry,
        )
