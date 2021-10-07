import math

import solid
import solid.utils
from solid import OpenSCADObject

from .utils import extrude, degree_to_radians


def pill(width: float, height: float, **kwargs) -> OpenSCADObject:
    """A pill-shaped object.

    Params:
            width (float): total width in mm
            height (float): total height in mm (or diameter on circular parts)
    """
    if width <= 0 or height <= 0:
        raise ValueError("Width and height should be positive values")

    radius = height / 2
    center_offset = width / 2 - radius
    return solid.hull()(
        solid.utils.left(center_offset)(solid.circle(r=radius, **kwargs)),
        solid.square((width - height, height), center=True),
        solid.utils.right(center_offset)(solid.circle(r=radius, **kwargs)),
    )


def button_hole(
    width: float, height: float, border: float, depth: float = None, **kwargs
) -> OpenSCADObject:
    """A pill shaped object with a hole inside.

    Params:
            width (float): width in mm
            height (float): height in mm (or diameter on circular parts)
            border (float): hole border in mm, if positive is added to a pill with
                            given dimension, otherwise is subtracted
            depth (float, optional): if given extrude the model
    """
    if height > width:
        raise ValueError("width should be greater than height")

    if border > 0:
        full = pill(width + 2 * border, height + 2 * border, **kwargs)
        hole = pill(width, height, **kwargs)
    elif border < 0:
        if 2 * border > height:
            raise ValueError("Subtractive border should be smaller than radius")

        full = pill(width, height, **kwargs)
        hole = pill(width + 2 * border, height + 2 * border, **kwargs)
    else:
        raise ValueError("Border should be a strictly positive or negative value")

    result = full - hole
    if depth is not None:
        result = extrude(result, depth)

    return result


def teeth(base: float, angle: float, length: float):
    angle_r = degree_to_radians(angle)
    x = base * math.cos(angle_r) ** 2
    y = base * math.sin(angle_r) * math.cos(angle_r)

    points = ((0, 0), (x, y), (base, 0))
    triangle = solid.polygon(points)
    return extrude(triangle, length)
