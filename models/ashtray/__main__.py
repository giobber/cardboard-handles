import math

import solid
import solid.utils
from loguru import logger

from models.system.config import load_toml, show_config
from models.system.constants import CONFIG_PATH, OUTPUT_PATH
from models.system.utils import render, set_color

from .config import AshtrayConfig


def parallelogram(width, height, angle):
    angle_r = angle * math.tau / 360
    offset = height / math.tan(angle_r)
    points = [(0, 0), (width, 0), (width + offset, height), (offset, height), (0, 0)]
    logger.debug(angle_r)
    logger.debug(points)
    return solid.polygon(points=points)


c: AshtrayConfig = load_toml(CONFIG_PATH / "ashtray.toml", AshtrayConfig)
show_config(c)


floor = solid.square((c.floor_radius, c.floor_thick))


angle = solid.utils.arc(rad=1, start_degrees=-90, end_degrees=0)
angle = solid.scale((c.wall_thick, c.floor_thick, 1))(angle)
angle = solid.translate((c.floor_radius, c.floor_thick, 0))(angle)


wall = solid.square((c.wall_thick, c.height - c.floor_thick))
wall = solid.translate((c.floor_radius, c.floor_thick, 0))(wall)


hang = solid.polygon(((0, 0), (c.hang_height, 0), (0, -c.hang_height)))
hang = solid.translate((c.floor_radius + c.wall_thick, c.height, 0))(hang)


draw = floor + angle + wall + hang
result = solid.rotate_extrude(360, segments=c.segments)(draw)
result = set_color(result, "Green")

hole = solid.cylinder(d=c.hole_diameter, h=c.hole_length, segments=c.segments)
hole = solid.rotate((0, 90 - c.hole_angle, 0))(hole)
hole = solid.translate((c.full_radius - c.hole_length, 0, c.height))(hole)

hole = set_color(hole, "red")

result -= solid.rotate((0, 0, 0))(hole)
result -= solid.rotate((0, 0, 90))(hole)
result -= solid.rotate((0, 0, 180))(hole)
result -= solid.rotate((0, 0, 270))(hole)

render(result, OUTPUT_PATH / "ashtray.scad")
