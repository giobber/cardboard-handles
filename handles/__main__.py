import pathlib

import solid
import solid.utils
from loguru import logger

from utils.config import load_toml


# TODO: move to module
def pill(width: float, diameter: float, **kwargs) -> solid.OpenSCADObject:
    center_distance = (width - diameter) / 2
    return solid.hull()(
        solid.utils.left(center_distance)(solid.circle(d=diameter, **kwargs)),
        solid.utils.right(center_distance)(solid.circle(d=diameter, **kwargs)),
    )


# TODO: move to module
def button_hole(
    width: float, diameter: float, border: float, **kwargs
) -> solid.OpenSCADObject:
    assert border > 0
    _full = pill(width + 2 * border, diameter + 2 * border, **kwargs)
    _hole = pill(width, diameter, **kwargs)
    return _full - _hole


def button_hole_3d(
    width: float, diameter: float, border: float, depth: float, **kwargs
) -> solid.OpenSCADObject:
    draw = button_hole(width, diameter, border, **kwargs)
    return solid.linear_extrude(depth)(draw)


CONFIG_PATH = pathlib.Path("./config")
OUTPUT_PATH = pathlib.Path("./output")

config = load_toml(CONFIG_PATH / "handles.toml", Config)


# inner Hole
# TODO: calculate external depth based on cardboard depth
inner_width = 100
inner_height = 35
cardboard_depth = 6


# External and internal mask pressing over cardboard
mask_border = 12
mask_depth = 2
mask_width = inner_width + 2 * mask_border
mask_height = inner_height + 2 * mask_border


# External part main body
# TODO: missing border clip to handle internal part
external_border = 3.5
external_depth = 17
external_width = inner_width + 2 * external_border
external_height = inner_height + 2 * external_border

mask = button_hole_3d(
    external_width, external_height, mask_border - external_border, mask_depth
)
external = button_hole_3d(inner_width, inner_height, external_border, external_depth)
external_part = mask + external
external_part = solid.color("ForestGreen")(external_part)


# Internal part main body
# TODO: missing tolerance to let parts slice together
internal_border = 1.5
internal_depth = 10
internal_width = external_width + 2 * internal_border
internal_height = external_height + 2 * internal_border

mask = button_hole_3d(
    internal_width,
    internal_height,
    mask_border - internal_border - external_border,
    mask_depth,
)
internal = button_hole_3d(
    external_width, external_height, internal_border, internal_depth
)
internal_part = mask + internal
internal_part = solid.color("Lime")(internal_part)


# Generate a composed solid
full = solid.union()
# full.add(solid.utils.forward(mask_height / 2 + 5)(external_part))
# full.add(solid.utils.back(mask_height / 2 + 5)(internal_part))
full.add(external_part)
full.add(solid.utils.up(mask_depth + cardboard_depth)(internal_part))


# Render
logger.info("Rendering...")
solid.scad_render_to_file(external_part, OUTPUT_PATH / "external.scad")
solid.scad_render_to_file(internal_part, OUTPUT_PATH / "internal.scad")
solid.scad_render_to_file(full, OUTPUT_PATH / "full.scad")
