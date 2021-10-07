import solid.utils
from loguru import logger

from models.system.config import load_toml, show_config
from models.system.constants import CONFIG_PATH, OUTPUT_PATH
from models.system.models import button_hole, teeth
from models.system.utils import render, set_color

from .config import Config

c = load_toml(CONFIG_PATH / "handles.toml", Config)
kwargs = dict(segments=c.segments)

show_config(c, ("tolerance", "lock_depth", "body_height", "hang_length"))


# External part
mask = button_hole(c.hole_width, c.hole_height, c.mask_border, c.mask_depth, **kwargs)
body = button_hole(c.hole_width, c.hole_height, c.body_border, c.hole_depth, **kwargs)

hang = teeth(c.hang_depth, 40, length=c.hang_length)
hang = solid.rotate((0, 90, 0))(hang)
hang_t = solid.translate((-c.hang_length / 2, c.body_height / 2, c.hole_depth))(hang)
hang_b = solid.mirror((0, 1, 0))(hang_t)

external = mask + body + hang_b + hang_t
external = set_color(external, "ForestGreen")


# Internal part
offset = c.body_border + c.tolerance - 0.2

width = c.hole_width + 2 * offset
height = c.hole_height + 2 * offset
border = c.mask_border - offset

mask = button_hole(width, height, border, c.mask_depth, **kwargs)
lock = button_hole(width, height, c.lock_border, c.lock_depth + c.mask_depth, **kwargs)

internal = mask + lock
internal = set_color(internal, "Lime")


# Complete design
full = solid.union()
if c.compose_full:
    full.add(external)
    full.add(solid.utils.up(c.mask_depth + c.cardboard_depth)(internal))
else:
    offset = c.hole_height / 2 + c.mask_border + 5
    full.add(solid.utils.forward(offset)(external))
    full.add(solid.utils.back(offset)(internal))


# Rendering
render(external, OUTPUT_PATH / "external.scad")
render(internal, OUTPUT_PATH / "internal.scad")
render(full, OUTPUT_PATH / "full.scad")
