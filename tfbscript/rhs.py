"""The 5-11 byte right-hand-side operand used by value opcodes."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from tfbscript.ansi import number, operator, rgb_square, type_
from tfbscript.reference import Reference
from tfbscript.string_table import StringTable

if TYPE_CHECKING:
    from tfbscript.binary import BinaryReader

_OPERATORS = {
    0: "+",
    1: "-",
    2: "*",
    3: "/",
}


@dataclass
class Rhs:
    tag: int = 0x00
    kind: str = "null"  # 'int' | 'float' | 'color' | 'pair' | 'reference' | 'expression'
    value: object = None
    operator: int | None = None
    rhs: "Rhs | None" = None

    @classmethod
    def read(
        cls,
        reader: "BinaryReader",
        global_refs: StringTable,
        local_refs: StringTable,
    ) -> "Rhs":
        """Parse a 5-11 byte TFB-Script RHS.

        Args:
            reader: BinaryReader positioned at the RHS.
            global_refs: the script's 2nd string table (globals) for name resolution.
            local_refs: the script's 3rd string table (locals) for name resolution.
        Returns:
            An Rhs.
        """

        # A reference is 5 bytes (tag + 4-byte ref) unless there's room left for
        # the 6-byte "op + value2" tail (11 bytes total), decided here from how
        # many bytes are left in the payload.
        #
        # This is a proxy, not what the engine does. Game.exe's real RHS reader
        # (FUN_0043fd20, shared by check value's and set value's constructors,
        # FUN_0042fc00 / FUN_0042fb50) has no length check at all -- it decides
        # whether to read the operator+second-operand tail by looking up the
        # already-resolved reference's type category live against the object
        # graph (scripts bind to actors that already exist, so that graph is
        # available at parse time). A static decoder can't replicate that lookup.
        #
        # It doesn't need to: the authoring tool made the same type-compatible-or-
        # not decision at compile time and sized payload_size to match, only
        # emitting the extra 6 bytes when it had already decided the tail
        # belongs. So checking remaining bytes against that already-shaped
        # boundary is a lossless proxy for the real decision, not a guess --
        # verified byte-exact (zero mismatches) against all 42,391 check
        # value::op-code / set value::op-code RHS reads in the shipped corpus.

        available = reader.size_remaining()
        tag = reader.read_u8()

        # Reference, optionally extended to an expression by an operator tail.
        if tag == 0x02:
            ref = Reference.read(reader, global_refs, local_refs)

            if available < 11:
                return cls(tag, "reference", ref)

            op = reader.read_u8()
            rhs = Rhs.read(reader, global_refs, local_refs)
            return cls(tag, "expression", ref, operator=op, rhs=rhs)

        # Integer
        if (tag & 0xF0) == 0x00:
            return cls(tag, "int", reader.read_i32())

        # Float -- the low nibble is a subtype variant (0x10, 0x11, ... all seen
        # in shipped scripts), not part of the kind selector; only the high
        # nibble picks the kind, same as the int/color/pair checks below.
        if (tag & 0xF0) in (0x10, 0x80):
            value = round(reader.read_f32(), 7)  # round for display
            return cls(tag, "float", value)

        # RGBA color
        if (tag & 0xF0) == 0x20:
            return cls(tag, "color", reader.read_rgba())

        # int16 pair
        if (tag & 0xF0) == 0x30:
            return cls(tag, "pair", (reader.read_i16(), reader.read_i16()))

        raise ValueError(f"Unknown RHS tag 0x{tag:02X}")

    def to_string(
        self,
        show_types: bool = False,
        do_reconstructs: bool = True,
    ) -> str:
        """Render this RHS as a readable, syntax-colored string."""

        if self.kind == "int":
            prefix = type_("Int32: ") if show_types else ""
            return prefix + number(self.value)

        if self.kind == "float":
            prefix = type_("Float: ") if show_types else ""
            return prefix + number(self.value)

        if self.kind == "color":
            r, g, b, a = cast(tuple[int, int, int, int], self.value)
            prefix = type_("Color32: ") if show_types else type_("Color")
            return prefix + rgb_square(r, g, b) + number(f"({r}, {g}, {b}, {a})")

        if self.kind == "pair":
            x, y = cast(tuple[int, int], self.value)
            prefix = type_("Pair16: ") if show_types else type_("Pair")
            return prefix + number(f"({x}, {y})")

        if self.kind == "reference":
            return f"Ref: {self.value}" if show_types else f"{self.value}"

        if self.kind == "expression":
            if self.operator is not None:
                op = _OPERATORS.get(self.operator, f"unknown_operator_{self.operator}")
                op = operator(op)
            else:
                op = "unknown_operator_None"

            left = f"Ref: {self.value}" if show_types else f"{self.value}"
            right = self.rhs.to_string(show_types) if self.rhs else "unknown_rhs_None"

            # `x + 0` / `x - 0` is the compiler's way of storing a bare
            # reference; reconstruct it back to just `x`.
            is_plus_minus_zero = (
                self.rhs is not None
                and self.rhs.kind == "int"
                and self.rhs.value == 0
                and self.operator in (0, 1)
            )
            if do_reconstructs and is_plus_minus_zero:
                return left
            return f"({left} {op} {right})"

        return f"Unknown({self.kind}): {self.value}"

    def __str__(self) -> str:
        return self.to_string()
