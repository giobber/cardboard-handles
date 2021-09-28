import dataclasses
import pathlib

import solid
import solid.utils

from .config import load_toml


@dataclasses.dataclass
class Config:
    pass


def button_hole(total_width: float, diameter: float, **kwargs) -> solid.OpenSCADObject:
    center_distance = (total_width - diameter) / 2
    return solid.hull()(
        solid.utils.left(center_distance)(solid.circle(d=diameter, **kwargs)),
        solid.utils.right(center_distance)(solid.circle(d=diameter, **kwargs)),
    )


def button_hole_3d(
    total_width: float, diameter: float, depth: float, **kwargs
) -> solid.OpenSCADObject:
    return solid.linear_extrude(depth)(button_hole(total_width, diameter, **kwargs))


CONFIG_PATH = pathlib.Path("./config")
OUTPUT_PATH = pathlib.Path("./output")

config = load_toml(CONFIG_PATH / "handles.toml", Config)


# inner Hole
inner_width = 100
inner_height = 35


# External and internal mask pressing over cardboard
mask_border = 12
mask_depth = 2
mask_width = inner_width + 2 * mask_border
mask_height = inner_height + 2 * mask_border

mask = button_hole_3d(mask_width, mask_height, mask_depth)


# External part main body
external_border = 3.5
external_depth = 17
external_width = inner_width + 2 * external_border
external_height = inner_height + 2 * external_border

external = button_hole_3d(external_width, external_height, external_depth)
external_hole = button_hole_3d(inner_width, inner_height, external_depth)


# Internal part main body
internal_border = 1.5
internal_depth = 10
internal_width = external_width + 2 * internal_border
internal_height = external_height + 2 * internal_border

internal = button_hole_3d(internal_width, internal_height, internal_depth)
internal_hole = button_hole_3d(external_width, external_height, internal_depth)


external_part = mask + external - external_hole
solid.scad_render_to_file(external_part, OUTPUT_PATH / "external.scad")


internal_part = mask + internal - internal_hole
solid.scad_render_to_file(internal_part, OUTPUT_PATH / "internal.scad")


full = solid.union()
full.add(solid.utils.forward(mask_height / 2 + 5)(external_part))
full.add(solid.utils.back(mask_height / 2 + 5)(internal_part))
solid.scad_render_to_file(full, OUTPUT_PATH / "full.scad")
