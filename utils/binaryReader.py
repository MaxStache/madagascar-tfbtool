import struct
from typing import TYPE_CHECKING

from TFBScriptRHS import TFBScriptRHS
from TFBScriptReference import TFBScriptReference

if TYPE_CHECKING:
    from TFBStringTable import TFBStringTable


class BinaryReader:
    def __init__(self, data: bytes, littleEndian=True):
        self.data = memoryview(data)
        self.offset = 0
        self.endian = "<" if littleEndian else ">"

    def tell(self):
        return self.offset

    def seek(self, offset):
        self.offset = offset

    def skip(self, n):
        self.offset += n

    def remaining(self):
        return self.data[self.offset :]

    def sizeRemaining(self) -> int:
        return len(self.data) - self.offset

    def eof(self):
        return self.offset >= len(self.data)

    def read(self, fmt):
        """
        unpacks and returns a single value and advances the offset by the size of the unpacked data
        """
        fmt = self.endian + fmt  # <X or >X
        size = struct.calcsize(fmt)
        value = struct.unpack_from(fmt, self.data, self.offset)
        self.offset += size
        return value[0]

    def readMultiple(self, fmt):
        """
        unpacks and return to a tuple and advances the offset by the size of the unpacked data
        """
        fmt = self.endian + fmt  # <XXX or >XXX
        size = struct.calcsize(fmt)
        value = struct.unpack_from(fmt, self.data, self.offset)
        self.offset += size
        return value

    def readBytes(self, n):
        data = self.data[self.offset : self.offset + n].tobytes()
        self.offset += n
        return data

    def readString(self, length, encoding="latin1"):
        return self.readBytes(length).decode(encoding)

    def readUint8(self) -> int:
        return self.read("B")

    def readUint32(self) -> int:
        return self.read("I")

    def readInt32(self) -> int:
        return self.read("i")

    def readFloat(self) -> int:
        return self.read("f")

    def readHalf(self) -> int:
        return self.read("h")

    def readRGBA(self) -> tuple[int, int, int, int]:
        r = self.readUint8()
        g = self.readUint8()
        b = self.readUint8()
        a = self.readUint8()
        return r, g, b, a


class PayloadBinaryReader(BinaryReader):
    """
    A BinaryReader that also stores a globalRefTable and localRefTable for reading TFBScriptReferences and TFBScriptRHS
    """

    def __init__(
        self,
        data: bytes,
        globalRefTable: TFBStringTable,
        localRefTable: TFBStringTable,
        littleEndian=True,
    ):
        super().__init__(data, littleEndian)
        self.globalRefTable = globalRefTable
        self.localRefTable = localRefTable

    def readRef(self) -> TFBScriptReference:
        """
        Reads a 4-byte TFB-Script variable reference.
        Returns:
            A TFBScriptReference representing the reference.
        """
        return TFBScriptReference.read(self, self.globalRefTable, self.localRefTable)

    def readRHS(self) -> TFBScriptRHS:
        """
        Reads a 5-11 byte TFB-Script RHS.
        Returns:
            A TFBScriptRHS representing the rhs.
        """
        return TFBScriptRHS.read(self, self.globalRefTable, self.localRefTable)
