import contextlib
import sys
from typing import Callable, Tuple
from random import randint
from math import sqrt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QMouseEvent, QPaintEvent, QCloseEvent
from PyQt5.QtCore import Qt, QTimer

from planet import PlanetBase, Planet
from gui import GuiCreator


class MainWindow(QMainWindow):
    BLACK = QColor(0, 0, 0)
    WHITE = QColor(255, 255, 255)
    RED = QColor(255, 0, 0)
    FPS = 60

    def __init__(
            self,
            min_width: int,
            min_height: int,
            starting_number_of_planets: int,
            max_number_of_planets: int,
            min_planet_mass: int,
            max_planet_mass: int,
            max_tracer_positions: int
    ) -> None:
        super().__init__()
        self.min_width = min_width
        self.min_height = min_height
        self.starting_number_of_planets = starting_number_of_planets
        self.max_number_of_planets = max_number_of_planets
        self.min_planet_mass = min_planet_mass
        self.max_planet_mass = max_planet_mass
        self.max_tracer_positions = max_tracer_positions

        self.setMinimumSize(self.min_width, self.min_height)
        self.setWindowTitle("Gravsim")

        self.timer = QTimer()
        self.update_simulation_speed()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()

        self.pause_button = None
        self.center_of_mass_button = None
        self.tracer_button = None

        self.displayed_selected_planet_info = None
        self.displayed_number_of_planets = None

        self.planet_x_edit_input = None
        self.planet_y_edit_input = None
        self.planet_mass_edit_input = None

        self.planets = []
        self.selected_planet = None
        self.paused_selected_planet = False
        self.create_planets(self.starting_number_of_planets)

        self.gui_creator = GuiCreator(self)
        self.create_gui(self.gui_creator)
        self.update_displayed_number_of_planets()
        self.update_selected_planet_info_label()

    def create_gui(self, gui_creator: GuiCreator) -> None:
        self.add_buttons(gui_creator.create_button)
        self.add_sliders(gui_creator.create_slider)
        self.add_info_labels(gui_creator.create_info_label)
        self.add_input_labels_to_edit_selected_planet(gui_creator.create_input_label)

    def add_buttons(self, create_button: Callable) -> None:
        data_to_create_buttons = [
            ("Pause", None, True),
            ("Center of mass", None, True),
            ("Tracer", self.toggle_tracer, True),
            ("Spawn planet", self.spawn_planet, False),
            ("Reset planets", self.reset_planets, False),
            ("Remove planet", self.remove_planet, False),
            ("Center planets", self.center_planets, False),
            ("Change properties", self.edit_all_selected_planet_properties, False)
        ]

        for i, (button_text, button_action, is_checkable) in enumerate(data_to_create_buttons):
            button = create_button(
                name=button_text,
                action=button_action,
                checkable=is_checkable,
                position=(10 + i * 100, 10),
                size=(100, 35)
            )

            match button_text:
                case "Pause":
                    self.pause_button = button
                case "Center of mass":
                    self.center_of_mass_button = button
                case "Tracer":
                    self.tracer_button = button
                case "Change properties":
                    button.move(310, 95)

    def add_sliders(self, create_slider: Callable) -> None:
        create_slider(
            position=(730, 10),
            size=(100, 20),
            action=self.update_simulation_speed
        )

    def add_info_labels(self, create_info_label: Callable) -> None:
        self.displayed_selected_planet_info = create_info_label(
            position=(10, 49),
            size=(300, 40),
        )
        self.displayed_number_of_planets = create_info_label(
            position=(320, 48),
            size=(115, 40),
            border_size=0
        )

    def add_input_labels_to_edit_selected_planet(self, create_input_label: Callable) -> None:
        data_to_create_input_labels = [
            (PlanetBase.X, self.edit_selected_planet_x_position),
            (PlanetBase.Y, self.edit_selected_planet_y_position),
            (PlanetBase.Mass, self.edit_selected_planet_mass)
        ]
        for i, (input_text, input_action) in enumerate(data_to_create_input_labels):
            input_label = create_input_label(
                text=input_text,
                action=input_action,
                position=(10 + i * 100, 95),
                size=(100, 35)
            )

            match input_text:
                case PlanetBase.X:
                    self.planet_x_edit_input = input_label
                case PlanetBase.Y:
                    self.planet_y_edit_input = input_label
                case PlanetBase.Mass:
                    self.planet_mass_edit_input = input_label

    def edit_all_selected_planet_properties(self) -> None:
        if self.selected_planet:
            self.edit_selected_planet_x_position()
            self.edit_selected_planet_y_position()
            self.edit_selected_planet_mass()

    def update_simulation_speed(self, value: int = 1) -> None:
        self.timer.setInterval(1000 // (self.FPS * value))

    def update_simulation(self) -> None:
        if self.selected_planet:
            self.update_selected_planet_info_label()

        if not self.pause_button.isChecked():
            for planet in self.planets:

                if planet == self.selected_planet and self.paused_selected_planet:
                    if planet.tracer_enabled:
                        planet.add_tracer_position()
                    continue

                for other_planet in self.planets:
                    if planet != other_planet:
                        dx = other_planet.x - planet.x
                        dy = other_planet.y - planet.y
                        distance = sqrt(dx ** 2 + dy ** 2)

                        force = (dx / distance, dy / distance)
                        planet.apply_force(force)

                planet.update()
        self.update()

    def toggle_tracer(self) -> None:
        for planet in self.planets:
            planet.tracer_enabled = not planet.tracer_enabled
            if not planet.tracer_enabled:
                planet.tracer_positions.clear()

    def create_planets(self, number_of_planets_to_create: int = 1, tracer: bool = False) -> bool:
        if len(self.planets) + number_of_planets_to_create <= self.max_number_of_planets:
            window_size = self.size()
            window_width = window_size.width()
            window_height = window_size.height()

            for _ in range(number_of_planets_to_create):
                x = randint(0, window_width)
                y = randint(0, window_height)
                mass = randint(self.min_planet_mass, self.max_planet_mass)
                planet = Planet(x, y, mass, tracer, max_tracer_positions=self.max_tracer_positions)
                self.planets.append(planet)

            return True
        return False

    def spawn_planet(self) -> bool:
        if self.create_planets():
            if self.tracer_button.isChecked():
                self.planets[-1].tracer_enabled = True

            self.update_displayed_number_of_planets()

            return True
        return False

    def reset_planets(self) -> None:
        if self.planets:
            self.planets.clear()
            self.selected_planet = None

        if self.tracer_button.isChecked():
            self.create_planets(self.starting_number_of_planets, True)
        else:
            self.create_planets(self.starting_number_of_planets)

        self.update_selected_planet_info_label()
        self.update_planet_info_input_label()
        self.update_displayed_number_of_planets()

    def remove_planet(self) -> bool:
        if self.planets:
            if self.selected_planet:
                self.planets.remove(self.selected_planet)
                self.selected_planet = None
                self.update_selected_planet_info_label()
                self.update_planet_info_input_label()
            else:
                self.planets.pop(0)

            self.update_displayed_number_of_planets()
            return True
        return False

    def center_planets(self) -> None:
        if not self.planets:
            return

        center_of_mass_x, center_of_mass_y = self.calculate_center_of_mass()
        window_size = self.size()
        center_of_window = {
            "x": window_size.width() // 2,
            "y": window_size.height() // 2
        }
        difference = {
            "x": center_of_window["x"] - center_of_mass_x,
            "y": center_of_window["y"] - center_of_mass_y,
        }

        for planet in self.planets:
            planet.x += difference["x"]
            planet.y += difference["y"]

            if planet.tracer_enabled:
                planet.tracer_positions = [
                    (
                        tracer_position[0] + difference["x"],
                        tracer_position[1] + difference["y"]
                    )
                    for tracer_position in planet.tracer_positions
                ]

    def edit_selected_planet_x_position(self) -> bool:
        if self.selected_planet:
            BLOCKED_ZONE = 100_000
            with contextlib.suppress(ValueError):
                inputted_x = float(self.planet_x_edit_input.text())
                if -BLOCKED_ZONE <= inputted_x <= BLOCKED_ZONE:
                    self.selected_planet.x = inputted_x
                    return True
        return False

    def edit_selected_planet_y_position(self) -> bool:
        if self.selected_planet:
            BLOCKED_ZONE = 100_000
            with contextlib.suppress(ValueError):
                inputted_y = float(self.planet_y_edit_input.text())
                if -BLOCKED_ZONE <= inputted_y <= BLOCKED_ZONE:
                    self.selected_planet.y = inputted_y
                    return True
        return False

    def edit_selected_planet_mass(self) -> bool:
        if self.selected_planet:
            with contextlib.suppress(ValueError):
                inputted_mass = int(self.planet_mass_edit_input.text())
                if self.min_planet_mass <= inputted_mass <= self.max_planet_mass:
                    self.selected_planet.mass = inputted_mass
                    self.selected_planet.radius = int(sqrt(inputted_mass))
                    return True
        return False

    def calculate_center_of_mass(self) -> Tuple[int, int] | None:
        if self.planets:
            total_mass = sum(planet.mass for planet in self.planets)
            center_x = int(sum(planet.x * planet.mass for planet in self.planets) / total_mass)
            center_y = int(sum(planet.y * planet.mass for planet in self.planets) / total_mass)
            return center_x, center_y
        return None

    def display_center_of_mass(self, painter: QPainter, pen_color: QColor, mark_size: int = 10) -> None:
        if not self.planets:
            return

        center_of_mass_x, center_of_mass_y = self.calculate_center_of_mass()
        painter.setPen(pen_color)
        painter.drawLine(
            center_of_mass_x, center_of_mass_y - mark_size,
            center_of_mass_x, center_of_mass_y + mark_size
        )
        painter.drawLine(
            center_of_mass_x - mark_size, center_of_mass_y,
            center_of_mass_x + mark_size, center_of_mass_y
        )

    def update_displayed_number_of_planets(self) -> None:
        self.displayed_number_of_planets.setText(
            f"Number of planets: {len(self.planets)}"
        )

    def update_selected_planet_info_label(self) -> None:
        if self.selected_planet:
            selected_planet_info = "Selected Planet: " \
                f"{PlanetBase.X}={int(self.selected_planet.x)}, " \
                f"{PlanetBase.Y}={int(self.selected_planet.y)}, " \
                f"{PlanetBase.Mass}={self.selected_planet.mass}"
        else:
            selected_planet_info = "No planet selected"

        self.displayed_selected_planet_info.setText(selected_planet_info)

    def update_planet_info_input_label(self) -> None:
        if self.selected_planet:
            self.planet_x_edit_input.setText(str(int(self.selected_planet.x)))
            self.planet_y_edit_input.setText(str(int(self.selected_planet.y)))
            self.planet_mass_edit_input.setText(str(self.selected_planet.mass))
            self.set_read_only_mode_for_info_input_fields(False)
        else:
            self.planet_x_edit_input.setText(PlanetBase.X)
            self.planet_y_edit_input.setText(PlanetBase.Y)
            self.planet_mass_edit_input.setText(PlanetBase.Mass)
            self.set_read_only_mode_for_info_input_fields()

    def set_read_only_mode_for_info_input_fields(self, only_readable_mode: bool = True) -> None:
        self.planet_x_edit_input.setReadOnly(only_readable_mode)
        self.planet_y_edit_input.setReadOnly(only_readable_mode)
        self.planet_mass_edit_input.setReadOnly(only_readable_mode)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.selected_planet:
            mouse_position = event.pos()
            self.selected_planet.x, self.selected_planet.y = mouse_position.x(), mouse_position.y()
            self.update_planet_info_input_label()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            mouse_position = event.pos()

            for planet in self.planets:
                if sqrt((planet.x - mouse_position.x()) ** 2 + (planet.y - mouse_position.y()) ** 2) <= planet.radius:
                    if planet != self.selected_planet:
                        self.selected_planet = planet
                        self.update_planet_info_input_label()
                    self.paused_selected_planet = True
                    return

            self.selected_planet = None
            self.update_selected_planet_info_label()
            self.update_planet_info_input_label()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.paused_selected_planet:
            self.paused_selected_planet = False

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.BLACK)

        for planet in self.planets:
            if planet == self.selected_planet:
                planet.draw(painter, self.RED, self.WHITE)
            else:
                planet.draw(painter, self.WHITE, self.WHITE)

        if self.center_of_mass_button.isChecked() and self.planets:
            self.display_center_of_mass(painter, self.RED)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(
        min_width=1000,
        min_height=800,
        starting_number_of_planets=5,
        max_number_of_planets=25,
        min_planet_mass=50,
        max_planet_mass=1000,
        max_tracer_positions=1000
    )
    main_window.show()
    sys.exit(app.exec_())
