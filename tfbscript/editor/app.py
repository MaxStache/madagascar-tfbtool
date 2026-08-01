# pyright: basic

import os
import signal
from pathlib import Path
from typing import cast

from tfbscript.ansi import set_colors_enabled
from tfbscript.script import ScriptFile

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory, QTreeWidget

from .fonts import register_bold_variant
from .style import build_palette, Win98TreeStyle
from .widgets import populate_tree

os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "0")
os.environ.setdefault("QT_SCALE_FACTOR", "1")

signal.signal(signal.SIGINT, signal.SIG_DFL)

set_colors_enabled(False)


def open_editor(script: ScriptFile):
    app = cast(QApplication, QApplication.instance()) or QApplication([])

    SCRIPT_DIR = Path(__file__).resolve().parent

    window = QMainWindow()
    window.setWindowTitle("TFBScript Editor")
    window.resize(700, 420)

    app.setStyle(Win98TreeStyle(QStyleFactory.create("Fusion")))

    QFontDatabase.addApplicationFont(
        str(Path(SCRIPT_DIR, "fonts", "ms-sans-serif", "MS Sans Serif.ttf"))
    )
    register_bold_variant(
        "MS Sans Serif",
        Path(SCRIPT_DIR, "fonts", "ms-sans-serif-bold", "MS Sans Serif Bold.ttf"),
    )

    font = QFont("MS Sans Serif")
    font.setPixelSize(13)
    app.setFont(font)

    app.setPalette(build_palette())

    def save() -> None:
        print("SAVE SAVE SAVE")

    file_menu = window.menuBar().addMenu("File")
    file_menu.addAction("Save").triggered.connect(save)

    tree = QTreeWidget()
    tree.setHeaderHidden(True)
    tree.setSelectionMode(QTreeWidget.SelectionMode.NoSelection)
    tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    tree.setRootIsDecorated(True)
    tree.setItemsExpandable(True)
    tree.setIndentation(40)
    tree.itemClicked.connect(
        lambda item, column: item.setExpanded(not item.isExpanded())
    )

    for opcode in script.instructions:
        populate_tree(tree, opcode)

    window.setCentralWidget(tree)
    window.show()

    app.exec()
