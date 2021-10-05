import math
import pathlib

import solid
import solid.utils
from loguru import logger

# TODO: move to a constants module
CONFIG_PATH = pathlib.Path("./config")
OUTPUT_PATH = pathlib.Path("./output")


def parallelogram(width, height, angle):
    angle_r = angle * math.tau / 360
    offset = height / math.tan(angle_r)
    points = [(0, 0), (width, 0), (width + offset, height), (offset, height), (0, 0)]
    logger.debug(angle_r)
    logger.debug(points)
    return solid.polygon(points=points)


diameter = 110  # External diameter (12 cm - .5 cm)
height = 30  # wall height (without floor and overhang)
border = 3  # Wall and floor border thickness

hang_angle = 40  # overhang angle
hang_offset = 10  # overhang offset

hole_diameter = 8  # cigarette hole

segments = 64

external_radius = diameter / 2
internal_radius = external_radius - border


floor = solid.square((internal_radius, border))


angle = solid.utils.arc(rad=border, start_degrees=-90, end_degrees=0)
angle = solid.translate((internal_radius, border, 0))(angle)


wall = solid.square((border, height))
wall = solid.translate((internal_radius, border, 0))(wall)


hang_angle_r = hang_angle * math.tau / 360
hang_height = hang_offset * math.tan(hang_angle_r)
hang = parallelogram(border, hang_height, hang_angle)
hang = solid.translate((internal_radius, height + border, 0))(hang)


draw = floor + angle + wall + hang

hole_length = diameter + 2 * hang_offset
hole_height = border + height + hang_height
hole = solid.cylinder(d=hole_diameter, h=hole_length, segments=segments)
hole = solid.utils.down(hole_length / 2)(hole)
hole_x = solid.utils.up(hole_height)(solid.rotate((90, 0, 0))(hole))
hole_y = solid.utils.up(hole_height)(solid.rotate((90, 0, 90))(hole))


result = solid.rotate_extrude(360, segments=segments)(draw)
result -= hole_x
result -= hole_y

solid.scad_render_to_file(result, OUTPUT_PATH / "ashtray.scad")
