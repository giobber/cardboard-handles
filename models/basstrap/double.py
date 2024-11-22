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

width = 200
base_height = 50
heng_height = 2


base = solid.cube((width, base_height, thickness))

hang = solid.cube((width, hang_height, thickness))
hang = rotate(hang, axis_x=45)

lateral = solid.polygon(((0, 0), (0, base_height), (hang_height / math.sqrt(2), hang_height / math.sqrt(2))))
lateral = extrude(lateral, thickness)
lateral = rotate(lateral, axis_y=-90)

result = base + hang + lateral

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
