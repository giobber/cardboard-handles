import dataclasses
import math


@dataclasses.dataclass
class AshtrayConfig:
    diameter: float = 110
    height: float = 42  # 2 + 30 + 10

    wall_thick: float = 2.0  # 5 * 0.4
    floor_thick: float = 1.4  # 5 * 0.28

    hang_height: float = 10  # overhang offset

    hole_diameter: float = 8
    hole_angle: float = 5

    segments: int = 128

    @property
    def floor_radius(self) -> float:
        return self.diameter / 2 - self.wall_thick

    @property
    def full_radius(self) -> float:
        return self.diameter / 2 + self.hang_height

    @property
    def hole_length(self) -> float:
        return math.sqrt(
            self.hang_height ** 2 + (self.hang_height + self.wall_thick) ** 2
        )
