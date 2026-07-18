from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.binaryReader import BinaryReader

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
    
    def getType(self) -> str:
        return self.string.split("::")[-1] # split by :: and get last part, wich is the type
    
    def getCategory(self) -> str | None:
        split_string = self.string.split("::")
        if len(split_string) > 2:
            return split_string[-2] # split by :: and get second to last part, wich is the category
        else:
            return None # no category, return None
        
    def getName(self) -> str:
        return self.string.split("::")[0] # split by :: and get first part, wich is the name


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
    
    def getAllWithType(self, typeName: str) -> list[TFBStringTable_Entry]:
        """
        Returns all entries in the string table that have a specific type.
        Examples of a type:
          - myactor::actor -> actor
          - myactor::behavior -> behavior
          - myactor::user::value -> value
        """
        matchingEntries = []
        for entry in self.entries:
            if entry.getType() == typeName:
                matchingEntries.append(entry)
        return matchingEntries
    
    def getAllWithCategory(self, categoryName: str) -> list[TFBStringTable_Entry]:
        """
        Returns all entries in the string table that have a specific category.
        Examples of a category:
          - myactor::actor -> None
          - myactor::behavior -> None
          - myactor::user::value -> user
        """
        matchingEntries = []
        for entry in self.entries:
            if entry.getCategory() == categoryName:
                matchingEntries.append(entry)
        return matchingEntries