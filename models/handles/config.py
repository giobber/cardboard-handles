import dataclasses
import math

from models.system.utils import degree_to_radians

@dataclasses.dataclass
class Config:
    hole_width: float = 90
    hole_height: float = 30
    hole_depth: float = 18

    mask_border: float = 10
    body_border: float = 3
    lock_border: float = 2

    mask_depth: float = 2
    hang_depth: float = 2
    cardboard_depth: float = 2

    hang_angle: float = 40

    segments: float = 64
    compose_full: bool = True

    @property
    def tolerance(self) -> float:
        angle_r = degree_to_radians(self.hang_angle)
        return self.hang_depth * math.sin(angle_r) * math.cos(angle_r)

    @property
    def lock_depth(self) -> float:
        return (
            self.hole_depth
            - self.hang_depth
            - self.mask_depth
            - self.cardboard_depth
            - self.mask_depth
        )

    @property
    def body_height(self):
        return self.hole_height + 2 * self.body_border

    @property
    def hang_length(self):
        return (self.hole_width - self.hole_height) * 0.8
