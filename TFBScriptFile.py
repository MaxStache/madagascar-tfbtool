from dataclasses import dataclass

from TFBStringTable import TFBStringTable
from opcodes.OpIfElse import COpIfElse
from utils.binaryReader import BinaryReader
from opcodes import COpCode
from opcodes.OpCode import OpParserContext


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

        # counter for 0xFF opcodes, wich are control blocks such as OpPrescript, OpStartup, OpShutdown, etc
        # we need to count them to know if its an OpPrescript(0), OpStartup(1), OpShutdown(2) or OpBehaviourImplementation(3,4,5,..)
        context = OpParserContext(opcodeTable, globalRefTable, localRefTable, controlBlockCounter=0)
        i = 0
        try:
            while i < instructionCount:
                instr = COpCode.read(reader, context)
                instructions.append(instr)

                i += instr.totalSpan()  # Count the instruction and its descendants

                if isinstance(instr, COpIfElse) and not instr.flags.noElse:
                    print("OpIf/Else HAS ELSE BRANCH")
                    raise NotImplementedError("OpIf/Else with else branch is not implemented yet")

        except Exception as e:
            print(f"\x1b[1;34mError reading instruction {i}: {e}\x1b[0m")
            raise

        return cls(
            magicString, unk, opcodeTable, globalRefTable, localRefTable, instructions
        )


if __name__ == "__main__":
    # Syntax coloring is auto-detected (on for a real terminal, off when piped
    # to a file/NO_COLOR is set) -- force it either way with:
    #   from utils.ansi_text import enable_colors, disable_colors
    #   disable_colors()

    with open("example_scripts/RW_WrongWayChecker.ai", "rb") as f:
        reader = BinaryReader(f.read(), littleEndian=True)
        file = TFBScriptFile.read(reader)
        for rootInstr in file.instructions:
            rootInstr.print()