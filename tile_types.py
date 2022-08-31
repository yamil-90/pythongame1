from typing import Tuple

import numpy as np

# structure the tile graphics to be compatible with console.tiles_rgb
graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# tile struct used for statically defined tyle data
tile_dt = np.dtype(
    [
        ("walkable", np.bool),
        ("transparent", np.bool),
        ("dark", graphic_dt), # Graphics for when this tile is not in FOV.
    ]
)


def new_tile(
        *,  # this enforces the use of keywords so that parameter order does not matter
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    # Helper function for defining individual tile types
    return np.array((walkable, transparent, dark), dtype=tile_dt)


floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
)
