import math

import solid
import solid.utils
from loguru import logger

from models.system.constants import CONFIG_PATH, OUTPUT_PATH
from models.system.utils import extrude, render, rotate, rotate_xy, set_color, translate

support_width: float = 10
hang_height: float = 20
thickness: float = 0.2 * 4
screw_hole_diameter: float = 2.0

depth: float = support_width
width: float = support_width + hang_height

base = solid.square((width, thickness))

hang = solid.square((hang_height * math.sqrt(2), thickness))
hang = rotate_xy(hang, 90 + 45)
hang = translate(hang, x=width, y=thickness)

draw = base + hang

result = extrude(draw, depth=depth)

screw_hole = solid.cylinder(d=screw_hole_diameter, h=thickness, segments=64)
screw_hole = rotate(screw_hole, axis_x=-90)
screw_hole = translate(screw_hole, x=support_width / 2, z=support_width / 2)
screw_hole = set_color(screw_hole, "blue")

result -= screw_hole

render(result, OUTPUT_PATH / "basstrap.scad")