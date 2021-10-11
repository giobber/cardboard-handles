import math

import solid
from loguru import logger


def degree_to_radians(angle_d: float):
    return angle_d * math.tau / 360


def set_color(obj: solid.OpenSCADObject, color: str):
    return solid.color(color)(obj)


def extrude(draw: solid.OpenSCADObject, depth: float) -> solid.OpenSCADObject:
    return solid.linear_extrude(depth)(draw)


def render(obj: solid.OpenSCADObject, path):
    logger.info(f"Rendering {path}")
    solid.scad_render_to_file(obj, path)


def rotate_xy(obj: solid.OpenSCADObject, angle: float) -> solid.OpenSCADObject:
    return solid.rotate(angle)(obj)


def rotate(
    obj: solid.OpenSCADObject,
    axis_x: float = 0.0,
    axis_y: float = 0.0,
    axis_z: float = 0.0,
) -> solid.OpenSCADObject:
    angles = (axis_x, axis_y, axis_z)
    return solid.rotate(angles)(obj)


def translate(
    obj: solid.OpenSCADObject, x: float = 0.0, y: float = 0.0, z: float = 0.0
) -> solid.OpenSCADObject:
    return solid.translate((x, y, z))(obj)
