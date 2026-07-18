from dataclasses import dataclass
from .OpCode import COpCode

@dataclass
class COpStartup(COpCode):
    @classmethod
    def readPayload(cls, reader, flags):
        return cls()

    def print(self, indent=0):
        print()
        super().print(indent)
        print(f"{' ' * 4 * indent}[ STARTUP: END ]\n")

    def toString(self):
        return "[ STARTUP ]"