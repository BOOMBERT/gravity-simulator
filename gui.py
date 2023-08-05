from typing import Callable, Tuple
from PyQt5.QtWidgets import QPushButton, QSlider, QLabel, QLineEdit, QMainWindow
from PyQt5.QtCore import Qt


class GuiCreator:
    def __init__(self, gui_window: QMainWindow) -> None:
        self.gui_window = gui_window

    def create_button(
            self,
            name: str,
            position: Tuple[int, int],
            size: Tuple[int, int],
            action: Callable = None,
            checkable: bool = False,
            background_color: str = "black",
            text_color: str = "white",
            hover_color: str = "rgb(225, 225, 225)",
            effect_text_color: str = "black",
            effect_background_color: str = "white",
            border_size: int = 1,
            border_type: str = "solid",
            border_color: str = "white"
    ) -> QPushButton:
        button = QPushButton(name, self.gui_window)
        button.setGeometry(*position, *size)

        standard_stylesheet = \
            "QPushButton { " \
            f"background-color: {background_color}; " \
            f"color: {text_color}; " \
            f"border: {border_size}px {border_type} {border_color}; " \
            "}" \
            "QPushButton:hover {" \
            f"color: {hover_color} ; " \
            "}"

        effect_stylesheet_components = \
            f"background-color: {effect_background_color} ;" \
            f"color: {effect_text_color}; "

        if checkable:
            button.setCheckable(True)
            button.setStyleSheet(
                f"{standard_stylesheet}"
                "QPushButton:checked {"
                f"{effect_stylesheet_components}"
                "}"
            )
        else:
            button.setStyleSheet(
                f"{standard_stylesheet}"
                "QPushButton:pressed {"
                f"{effect_stylesheet_components}"
                "}"
            )

        if action:
            button.clicked.connect(action)

        return button

    def create_slider(
            self,
            position: Tuple[int, int],
            size: Tuple[int, int],
            action: Callable,
            color: str = "white",
            hover_color: str = "rgb(225, 225, 225)",
            min_value: int = 1,
            max_value: int = 10,
            start_value: int = 1,
    ) -> QSlider:
        slider = QSlider(Qt.Horizontal, self.gui_window)
        slider.setGeometry(*position, *size)
        slider.setStyleSheet(
            "QSlider::handle:horizontal { "
            f"  background: {color}"
            "}"
            "QSlider::handle:horizontal:hover {"
            f"  background: {hover_color};"
            "}"
        )

        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(start_value)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.valueChanged.connect(action)

        return slider

    def create_info_label(
            self,
            position: Tuple[int, int],
            size: Tuple[int, int],
            text_color: str = "white",
            border_size: int = 1,
            border_type: str = "solid",
            border_color: str = "white"
    ) -> QLabel:
        info_label = QLabel(self.gui_window)
        info_label.setGeometry(*position, *size)
        info_label.setStyleSheet(
            f"color: {text_color}; "
            f"border: {border_size}px {border_type} {border_color}"
        )

        return info_label

    def create_input_label(
            self,
            text: str,
            action: Callable,
            position: Tuple[int, int],
            size: Tuple[int, int],
            background_color: str = "black",
            text_color: str = "white",
            border_size: int = 1,
            border_type: str = "solid",
            border_color: str = "white"
    ) -> QLineEdit:
        input_label = QLineEdit(self.gui_window)
        input_label.setGeometry(*position, *size)
        input_label.setStyleSheet(
            f"background-color: {background_color}; "
            f"color: {text_color}; "
            f"border: {border_size}px {border_type} {border_color};"
        )
        input_label.setText(text)
        input_label.setReadOnly(True)
        input_label.returnPressed.connect(action)

        return input_label
