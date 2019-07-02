import numpy as np


def optical_density(tile):
    """
    Convert a tile to optical density values.
    Args:
      tile: A 3D NumPy array of shape (tile_size, tile_size, channels).
    Returns:
      A 3D NumPy array of shape (tile_size, tile_size, channels)
      representing optical density values.
    """
    tile = tile.astype(np.float64)
    #od = -np.log10(tile/255 + 1e-8)
    od = -np.log((tile+1)/240)
    return od
