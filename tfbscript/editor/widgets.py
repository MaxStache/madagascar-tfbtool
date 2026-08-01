# pyright: basic

from collections.abc import Callable

from tfbscript.opcodes.base import Opcode

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)

from .style import Win98TreeStyle, tfb_colored_box


def clear_layout(layout: QHBoxLayout):
    while layout.count():
        item = layout.takeAt(0)
        if item is None:
            continue
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()


def opcode_row(opcode: Opcode, layout: QHBoxLayout, on_change: Callable[[], None]):
    fields = opcode.editor_repr().get("fields", [])

    for field in fields:
        f_type = field.get("type")

        if f_type == "op-label":
            label = QLabel(field.get("value", ""))
            tfb_colored_box(label, "#0000AA")
            layout.addWidget(label)

        elif f_type == "behavior-label":
            label = QLabel(field.get("value", ""))
            tfb_colored_box(label, "#00AA31")
            layout.addWidget(label)

        elif f_type == "block-label":
            label = QLabel(field.get("value", ""))
            label.setStyleSheet("font-weight: bold;")
            layout.addWidget(label)

        elif f_type == "label":
            label = QLabel(field.get("content", ""))
            label.setStyleSheet("font-weight: bold;")
            layout.addWidget(label)

        elif f_type == "string":
            label = QLabel(field.get("value", ""))
            label.setStyleSheet("color: #8A8880;")
            layout.addWidget(label)

        elif f_type == "rhs":
            content = str(field.get("rhs", None))
            label = QLabel(content)
            tfb_colored_box(label, "#616161")
            layout.addWidget(label)

        elif f_type == "ref":
            content = str(field.get("ref", None))
            label = QLabel(content)
            tfb_colored_box(label, "#616161")
            layout.addWidget(label)

        elif f_type == "enum":
            selected = field.get("entry", field.get("value", None))
            attr_name = field.get("name")

            button = QPushButton(str(selected))
            button.setFlat(True)
            button.setStyleSheet(
                "QPushButton { padding: 2px 4px; margin: 0px; border: none; background-color: #616161; color: #FFFFFF; }"
                " QPushButton::menu-indicator { image: none; width: 0px; height: 0px; }"
            )
            layout.addWidget(button)
            menu = QMenu(button)
            menu.setStyleSheet(
                "QMenu { background-color: #3c3c3c; color: #e0e0e0; border: 1px solid #555; padding: 2px; }"
                " QMenu::item { padding: 4px 16px; }"
                " QMenu::item:selected { background-color: #5a5a5a; color: #ffffff; }"
            )

            def select_entry(entry: object, attr_name: str | None = attr_name) -> None:
                if attr_name is not None:
                    setattr(opcode, attr_name, entry)
                on_change()

            for entry in selected.__class__:
                action = menu.addAction(str(entry))
                action.triggered.connect(
                    lambda checked=False, entry=entry: select_entry(entry)
                )

            button.setMenu(menu)

        else:
            raise NotImplementedError(f"Unsupported field type: {f_type}")


def populate_tree(parent: QTreeWidget | QTreeWidgetItem, opcode: Opcode):
    item = QTreeWidgetItem(parent)
    item.setExpanded(False)

    tree = item.treeWidget()

    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(Win98TreeStyle.CONTENT_OFFSET, 6, 0, 6)
    layout.setSpacing(4)
    layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

    def rerender_row() -> None:
        clear_layout(layout)
        opcode_row(opcode, layout, rerender_row)
        layout.addStretch()

    rerender_row()

    tree.setItemWidget(item, 0, container)
    context = opcode.context
    if context is not None:
        context.open_opcodes.append(opcode)

    try:
        for child in opcode.children:
            populate_tree(item, child)
    finally:
        if context is not None:
            context.open_opcodes.pop()
