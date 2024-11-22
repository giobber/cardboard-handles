import math

import solid
import solid.utils
from loguru import logger

from models.system.constants import CONFIG_PATH, OUTPUT_PATH
from models.system.utils import extrude, render, rotate, rotate_xy, set_color, translate

panel_depth: float = 240
panel_side: float = 120
panel_flat_border: float = 20

base_thickness: float = 0.4 * 2
base_border: float = 10

panel = solid.polygon(((0, 0), (panel_side, 0), (0, panel_side)))
panel = extrude(panel, panel_depth)
panel = set_color(panel, "#555555")

bb = base_border

support_base = solid.polygon(((0, 0), (0, panel_side), (panel_side, 0)))
support_hole = solid.polygon(
    (
        (bb, bb),
        (bb, panel_side - (1 + math.sqrt(2)) * bb),
        (panel_side - (1 + math.sqrt(2)) * bb, bb),
    )
)

support_base = extrude(support_base - support_hole, base_thickness)
support_base = set_color(support_base, "black")

lateral = solid.polygon(
    (
        (0, 0),
        (panel_flat_border, 0),
        (panel_flat_border, base_thickness),
        (0, base_thickness + panel_flat_border),
    )
)
lateral = extrude(lateral, base_thickness)
lateral = set_color(lateral, "black")
lateral = rotate(lateral, axis_x=90)

lateral = lateral + translate(rotate(lateral, axis_z=90), x=-base_thickness)


result = support_base + translate(panel, z=base_thickness) + lateral

# support_width: float = 10
# hang_height: float = 20
# thickness: float = 0.2 * 4
# screw_hole_diameter: float = 2.0
#
# depth: float = support_width
# width: float = support_width + hang_height
#
# base = solid.square((width, thickness))
# base = extrude(base, depth=depth + thickness)
# base = set_color(base, "green")
#
# hang = solid.square((hang_height * math.sqrt(2), thickness))
# hang = rotate_xy(hang, 90 + 45)
# hang = translate(hang, x=width, y=thickness)
# hang = extrude(hang, depth=depth + thickness)
# hang = set_color(hang, "blue")
#
# leg = solid.square((thickness, hang_height))
# leg = translate(leg, x=support_width)
# leg = extrude(leg, thickness)
# leg = set_color(leg, "purple")
#
# screw_hole = solid.cylinder(d=screw_hole_diameter, h=thickness, segments=64)
# screw_hole = rotate(screw_hole, axis_x=-90)
# screw_hole = translate(screw_hole, x=support_width / 2, z=support_width / 2)
# screw_hole = set_color(screw_hole, "red")
#
# result = base + hang + leg - screw_hole

render(result, OUTPUT_PATH / "basstrap.scad")
