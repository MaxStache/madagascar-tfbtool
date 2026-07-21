"""Enums shared by opcode payloads."""

from enum import IntEnum
from typing import override


# fmt: off
class RelOp(IntEnum):
    """Relational operator for OpCheckValue / OpFindSubset."""

    LessOrEq  = 0  # <=
    Eq        = 1  # ==
    GreatOrEq = 2  # >=
    Less      = 3  # <
    Great     = 4  # >
    NotEq     = 5  # !=

    def symbol(self) -> str:
        return ("<=", "==", ">=", "<", ">", "!=")[self.value]
    
    @override
    def __str__(self) -> str:
        return str(self.symbol())
    
class ControlRequirement(IntEnum):
    """u8 in OpControl payload that specifies how the control block is executed."""

    # the target must already satisfy the "controllable/active" check right now, or the block is skipped.
    Strict  = 0 # default, this is behavior when the byte isnt present in payload!

    #that requirement is relaxed, so the block runs even if the target isn't in that fully-ready state yet.
    Lenient = 1

    @override
    def __str__(self) -> str:
        return ("strict", "lenient")[self.value]
    
class CutsceneCommand(IntEnum):
    # TODO: TODO: TODO: Verify and figure out 0
    Unknown = 0
    Pause  = 1
    Resume = 2
    Start  = 3

    @override
    def __str__(self) -> str:
        return ("pause", "resume", "start")[self.value-1]
    
class SetDirection(IntEnum):
    """Direction for how to traverse a set"""

    forward = 0
    backward = 1
    randomly = 2

    @override
    def __str__(self) -> str:
        return ("forward", "backward", "randomly")[self.value]
    
class CombineMode(IntEnum):
    """Displacement combine mode for OpDisplace."""

    relative = 0
    absolute = 1
    local = 2

    @override
    def __str__(self) -> str:
        return ("relative", "absolute", "local")[self.value]
    
class MembershipTest(IntEnum):
    """Membership test for OpCheckMembership."""

    includes = 0  # set_a includes element_a
    excludes = 1  # set_a excludes element_a
    intersects_with = 2  # set_a intersects with_b (set_a has at least one element in common with set_b)
    includes_all = 3  # set_a all in set_b

    def symbol(self) -> str:
        # assumes format is "set_a <membership_test> element_a" or "set_a <membership_test> set_b"
        return ("in", "not in", "intersects with", "all in")[self.value]

class MembershipCombiner(IntEnum):
    """Membership combiner for OpChangeMembership."""

    include        = 0 # add a single thing?
    exclude        = 1 # remove a single thing?
    intersect_with = 2 
    be_replaced_by = 3  
    add            = 4  # concat sets together?
    exclude_all    = 5  # remove all elements that are also in set b?

    def symbol(self) -> str:
        # assumes format is "set_a.<membership_combiner>(element_a)" or "set_a.<membership_combiner>(set_b)"
        return ("include", "remove", "intersectWith", "replaceWith", "add", "removeAll")[self.value]


# fmt: on
