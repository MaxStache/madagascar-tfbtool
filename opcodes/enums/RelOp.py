from enum import IntEnum


# fmt:off
class ERelOp(IntEnum):
    """Relational operator for OpAbstractCheckValue / OpCheckValue."""

    LessOrEq  = 0  # <=
    Eq        = 1  # ==
    GreatOrEq = 2  # >=
    Less      = 3  # <
    Great     = 4  # >
    NotEq     = 5  # !=

    def symbol(self) -> str:
        return ("<=", "==", ">=", "<", ">", "!=")[self.value]
# fmt:on