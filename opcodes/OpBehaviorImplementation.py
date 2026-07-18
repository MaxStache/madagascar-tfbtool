from dataclasses import dataclass
from typing import Union

from TFBStringTable import TFBStringTable_Entry
from .OpCode import COpCode

@dataclass
class COpBehaviorImplementation(COpCode):
    _behaviorEntry: Union[TFBStringTable_Entry, None] = None  # This will hold the behavior entry from the localRefTable used for printing etc.

    @classmethod
    def readPayload(cls, reader, flags):
        return cls()
    
    def print(self, indent=0):
        print()
        super().print(indent)
        print(f"{' ' * 4 * indent}[ Behavior {self._behaviorEntry.getName() if self._behaviorEntry else "Failed to resolve"}: END ]\n")

    def toString(self):
        return f"[ Behavior: {self._behaviorEntry.getName() if self._behaviorEntry else "Failed to resolve"} ]"