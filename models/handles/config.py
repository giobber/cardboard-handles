import dataclasses


@dataclasses.dataclass
class Config:
    hole_width: float = 90
    hole_height: float = 30

    mask_border: float = 10
    body_border: float = 3
    lock_border: float = 2

    mask_depth: float = 2
    lock_depth: float = 8
    hang_depth: float = 2

    tolerance: float = 1
    cardboard_depth: float = 2

    compose_full: bool = False

    @property
    def body_depth(self):
        return (
            self.mask_depth
            + self.cardboard_depth
            + self.mask_depth
            + self.lock_depth
            + self.hang_depth
        )
