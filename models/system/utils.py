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
