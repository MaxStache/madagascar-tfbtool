import struct

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
        data = self.data[self.offset:self.offset+n].tobytes()
        self.offset += n
        return data

    def readString(self, length, encoding="latin1"):
        return self.readBytes(length).decode(encoding)
    
    def readUint8(self) -> int:
        return self.read("B")
    
    def readUint32(self) -> int:
        return self.read("I")