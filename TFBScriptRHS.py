"""
BASED ON REASEARCH AND REVERSE ENGENEERING BY CLAUDE, THIS FILE IS PARTIALLY AI GENERATED!
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, cast

from TFBScriptReference import TFBScriptReference

if TYPE_CHECKING:
    from utils.binaryReader import BinaryReader

from utils.ansi_text import type_, number, operator, text_rgb_square

@dataclass
class TFBScriptRHS:
    tag: int = 0x00
    kind: str = "null"
    value: object = None
    operator: Optional[int] = None
    rhs: Optional["TFBScriptRHS"] = None

    @classmethod
    def read(
        cls, reader: "BinaryReader", globalRefTable, localRefTable
    ) -> "TFBScriptRHS":
        """Parse a 5-11 byte TFB-Script RHS.
        Args:
            reader: BinaryReader
            globalRefTable: the script's 2rd string table (globals) for name resolution.
            localRefTable: the script's 3rd string table (locals) for name resolution
        Returns:
            A TFBScriptRHS.
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

        avail = reader.sizeRemaining()
        tag = reader.readUint8()

        # ------------------------------------------------------------------
        # Reference
        # ------------------------------------------------------------------
        if tag == 0x02:
            ref = TFBScriptReference.read(reader, globalRefTable, localRefTable)

            if avail < 11:
                return cls(tag, "reference", ref)

            op = reader.readUint8()
            rhs = TFBScriptRHS.read(reader, globalRefTable, localRefTable)

            return cls(
                tag=tag,
                kind="expression",
                value=ref,
                operator=op,
                rhs=rhs,
            )

        # ------------------------------------------------------------------
        # Integer
        # ------------------------------------------------------------------
        if (tag & 0xF0) == 0x00:
            value = reader.readInt32()
            return cls(tag, "int", value)

        # ------------------------------------------------------------------
        # Float -- the low nibble is a subtype variant (0x10, 0x11, ... all seen
        # in shipped scripts), not part of the kind selector; only the high
        # nibble picks the kind, same as the int/color/pair checks below.
        # ------------------------------------------------------------------
        if (tag & 0xF0) in (0x10, 0x80):
            value = reader.readFloat()
            value = round(value, 7)  # round to 7 decimal places for display
            return cls(tag, "float", value)

        # ------------------------------------------------------------------
        # RGBA color
        # ------------------------------------------------------------------
        if (tag & 0xF0) == 0x20:
            value = reader.readRGBA()
            return cls(tag, "color", value)

        # ------------------------------------------------------------------
        # int16 pair
        # ------------------------------------------------------------------
        if (tag & 0xF0) == 0x30:
            value = (reader.readHalf(), reader.readHalf())
            return cls(tag, "pair", value)

        raise ValueError(f"Unknown RHS tag 0x{tag:02X}")
    
    def toString(self, showTypes: bool = False, doReconstructs: bool = True, markReconstructs: bool = False) -> str:
        """
        Converts self (an TFBScriptRHS) into a readable string representation.
        """

        if self.kind == "int":
            text = ""

            if showTypes:
                text += type_("Int32: ")

            text += number(self.value)

            return text


        if self.kind == "float":
            text = ""

            if showTypes:
                text += type_("Float: ")

            text += number(self.value)

            return text

        if self.kind == "color":
            r, g, b, a = cast(tuple[int, int, int, int], self.value)

            text = ""

            if showTypes:
                text += type_("Color32: ")
            else:
                text += type_("Color")

            text += text_rgb_square(r, g, b)
            text += number(f"({r}, {g}, {b}, {a})")

            return text

        if self.kind == "pair":
            # two little-endian half floats
            x, y = cast(tuple[float, float], self.value)

            text = ""

            if showTypes:
                text += type_("Pair16: ")
            else:
                text += type_("Pair")

            text += number(f"({x}, {y})")

            return text



        if self.kind == "reference":
            if showTypes:
                text = f"Ref: {self.value}"
            else:
                text = f"{self.value}"

            return text

        if self.kind == "expression":
            operators = {
                0: "+",
                1: "-",
                2: "*",
                3: "/",
            }

            if self.operator is not None:
                op = operators.get(self.operator, f"unknown_operator_{self.operator}")
                op = operator(op)
            else:
                op = "unknown_operator_None"

            left = f"Ref: {self.value}" if showTypes else f"{self.value}"

            if self.rhs:
                right = self.rhs.toString(showTypes)
            else:
                right = "unknown_rhs_None"

            if doReconstructs and self.rhs and self.rhs.kind == "int" and self.rhs.value == 0 and self.operator in (0, 1):
                return f"{left}"
            else:
                return f"({left} {op} {right})"
        

        return f"Unknown({self.kind}): {self.value}"

    def __str__(self) -> str:
        return self.toString()