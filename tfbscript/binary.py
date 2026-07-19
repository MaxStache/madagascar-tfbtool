"""A small binary reader over an in-memory buffer."""

import struct


class BinaryReader:
    def __init__(self, data: bytes, little_endian: bool = True):
        self.data = memoryview(data)
        self.offset = 0
        self.endian = "<" if little_endian else ">"

    def tell(self) -> int:
        return self.offset

    def seek(self, offset: int) -> None:
        self.offset = offset

    def skip(self, count: int) -> None:
        self.offset += count

    def size_remaining(self) -> int:
        return len(self.data) - self.offset

    def eof(self) -> bool:
        return self.offset >= len(self.data)

    def read(self, fmt: str):
        """Unpack a single value and advance the offset by its size."""
        fmt = self.endian + fmt
        value = struct.unpack_from(fmt, self.data, self.offset)[0]
        self.offset += struct.calcsize(fmt)
        return value

    def read_bytes(self, count: int) -> bytes:
        data = self.data[self.offset : self.offset + count].tobytes()
        self.offset += count
        return data

    def read_string(self, length: int, encoding: str = "latin1") -> str:
        return self.read_bytes(length).decode(encoding)

    def read_u8(self) -> int:
        return self.read("B")

    def read_u32(self) -> int:
        return self.read("I")

    def read_i16(self) -> int:
        return self.read("h")

    def read_i32(self) -> int:
        return self.read("i")

    def read_f32(self) -> float:
        return self.read("f")

    def read_rgba(self) -> tuple[int, int, int, int]:
        return (self.read_u8(), self.read_u8(), self.read_u8(), self.read_u8())
