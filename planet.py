from typing import Tuple
from math import sqrt
from PyQt5.QtGui import QPainter, QColor


class PlanetBase:
    X: str = "X"
    Y: str = "Y"
    Mass: str = "Mass"


class Planet:
    def __init__(
            self,
            x: int,
            y: int,
            mass: int,
            tracer_enabled: bool = False,
            max_tracer_positions: int = 1000
    ) -> None:
        self.x = x
        self.y = y
        self.mass = mass
        self.tracer_enabled = tracer_enabled
        self.max_tracer_positions = max_tracer_positions
        self.radius = int(sqrt(mass))

        self.x_velocity = 0
        self.y_velocity = 0

        self.tracer_positions = []

    def apply_force(self, force: Tuple[float]) -> None:
        ax = force[0] / self.mass
        ay = force[1] / self.mass
        self.x_velocity += ax
        self.y_velocity += ay

    def update(self) -> None:
        self.x += self.x_velocity
        self.y += self.y_velocity

        if self.tracer_enabled:
            self.add_tracer_position()

    def add_tracer_position(self) -> None:
        self.tracer_positions.append((int(self.x), int(self.y)))
        if len(self.tracer_positions) > self.max_tracer_positions:
            self.tracer_positions.pop(0)

    def draw(self, painter: QPainter, pen_color: QColor, brush_color: QColor) -> None:
        painter.setPen(pen_color)
        painter.setBrush(brush_color)
        painter.drawEllipse(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2, self.radius * 2
        )

        if self.tracer_enabled:
            for tracer_position in self.tracer_positions:
                painter.drawPoint(*tracer_position)
