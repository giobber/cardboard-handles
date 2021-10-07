import solid
import solid.utils
from solid import OpenSCADObject


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
        solid.utils.right(center_offset)(solid.circle(r=radius, **kwargs)),
    )


def button_hole(width: float, height: float, border: float, **kwargs) -> OpenSCADObject:
    """A pill shaped object with a hole inside.

    Params:
            width (float): width in mm
            height (float): height in mm (or diameter on circular parts)
            border (float): hole border in mm, if positive is added to a pill with
                            given dimension, otherwise is subtracted
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

    return full - hole


def button_hole_3d(
    width: float, diameter: float, border: float, depth: float, **kwargs
) -> OpenSCADObject:
    draw = button_hole(width, diameter, border, **kwargs)
    return solid.linear_extrude(depth)(draw)
