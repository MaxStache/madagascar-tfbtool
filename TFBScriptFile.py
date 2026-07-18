from dataclasses import dataclass

from lib.binaryReader import BinaryReader
from opcodes import COpCode
from opcodes.OpCode import InstructionFlags


@dataclass
class TFBStringTable_Entry:
    """
    Represents a single entry in a TFB string table
    """

    string: str  # u8 string length followed by string bytes
    metadata: bytes  # 4 bytes of metetadata usually 0x0

    @classmethod
    def read(cls, reader: BinaryReader):
        """
        Reads a TFBStringTable_Entry from a binary reader
        """

        stringLength = reader.readUint8()
        string = reader.readString(stringLength)
        metadata = reader.readBytes(4)

        return cls(string, metadata)


@dataclass
class TFBStringTable:
    """
    Represents one of the string tables in a TFB script file
    """

    entries: list[TFBStringTable_Entry]  # u32 entry count followed by entries

    @classmethod
    def read(cls, reader: BinaryReader):
        """
        Reads a TFBStringTable from a binary reader
        """

        entryCount = reader.readUint32()
        entries = [TFBStringTable_Entry.read(reader) for _ in range(entryCount)]

        return cls(entries)


@dataclass
class TFBScriptFile:
    """
    Represents a TFB script (.AI) file
    """

    magicString: str
    unk: bytes

    opcodeTable: TFBStringTable
    globalRefTable: TFBStringTable
    localRefTable: TFBStringTable

    instructions: list[COpCode]

    @classmethod
    def read(cls, reader: BinaryReader):
        """
        Reads a TFBScriptFile from a binary reader
        """

        magicStringLength = reader.readUint8()
        magicString = reader.readString(magicStringLength)

        unk = reader.readBytes(4)

        opcodeTable = TFBStringTable.read(reader)
        globalRefTable = TFBStringTable.read(reader)
        localRefTable = TFBStringTable.read(reader)

        instructions = []
        instructionCount = reader.readUint32()
        for _ in range(instructionCount):
            COpCode.read(reader, opcodeTable, globalRefTable, localRefTable)

        return cls(
            magicString, unk, opcodeTable, globalRefTable, localRefTable, instructions
        )


if __name__ == "__main__":
    with open("example_scripts/RW_Kids_Cup.ai", "rb") as f:
        reader = BinaryReader(f.read(), littleEndian=True)
        TFBScriptFile.read(reader)
