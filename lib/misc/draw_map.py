# lib/map/visualization.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
from typing import Optional, Tuple
from pathlib import Path

from lib.map.map import Map
from lib.map.tile import NextConnect


def calculate_tile_positions(tile_map: Map) -> Tuple[np.ndarray, dict]:
    """
    Calculate proper tile positions based on connection points.
    Returns:
        - base_coords: Array of (x,y) coordinates for each point in the map
        - tile_rects: Dict of {tile_index: (x, y, width, height)}
    """
    tile_positions = {}
    tile_rects = {}
    current_x, current_y = 0, 0


    for t, tile in enumerate(tile_map.tiles):
        # n = tile.n-1
        width = tile.width-1
        height = tile.height-1
        # if t == 0:
        #     width, height = height, width
        # Store tile position and dimensions
        tile_positions[t] = (current_x, current_y)
        tile_rects[t] = (current_x, current_y, width, height)

        TILE_MARGIN = 0.1

        # Calculate position for next tile based on connection
        if t < len(tile_map.tiles) - 1:
            next_conn = tile.next_conn
            if next_conn == NextConnect.RIGHT:
                current_x += width + TILE_MARGIN
            elif next_conn == NextConnect.LEFT:
                current_x -= width + TILE_MARGIN
            elif next_conn == NextConnect.TOP:
                current_y -= height + TILE_MARGIN
            elif next_conn == NextConnect.BOTTOM:
                current_y += height + TILE_MARGIN

    # Create coordinate mapping for all points
    base_coords = np.zeros((tile_map.get_total_n(), 2))
    for t, curve in enumerate(tile_map.tile_curves):
        tile_x, tile_y = tile_positions[t]
        width = tile_map.tiles[t].width
        height = tile_map.tiles[t].height
        # if t == 0:
        #     tile_x, tile_y = tile_y, tile_x
        for x in range(height):
            for y in range(width):
                hilbert_idx = curve[y, x]
                base_coords[hilbert_idx] = [tile_x + x, tile_y + y]

    return base_coords, tile_rects


def visualize_map(tile_map: Map,
                  proc_mapping: np.array,
                  save_as: Optional[str] = None,
                  show: bool = True,
                  dpi: int = 100,
                  linewidth: float = 1.5,
                  figsize: Tuple[int, int] = (10, 10)) -> plt.Figure:
    """
    Professional visualization of the complete Hilbert curve across all tiles.

    Args:
        tile_map: Initialized Map object
        proc_mapping: Mapping of hilbert index to processor
        save_as: Path to save the visualization
        show: Whether to display the plot
        dpi: Image resolution
        linewidth: Width of curve lines
        figsize: Figure dimensions in inches

    Returns:
        matplotlib Figure object
    """
    # Calculate proper tile positions
    base_coords, tile_rects = calculate_tile_positions(tile_map)
    # print(base_coords)

    # Create line segments for the entire curve
    segments = np.array([base_coords[:-1], base_coords[1:]]).transpose(1, 0, 2)
    # print(segments)
    segment_values = proc_mapping[1:]
    cmap = plt.get_cmap('rainbow')
    plt.figure(figsize=(7, 7))
    norm = plt.Normalize(vmin=segment_values.min(), vmax=segment_values.max())
    segment_colors = cmap(norm(segment_values))

    # Create figure
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    lc = LineCollection(segments, linewidth=linewidth, colors=segment_colors)
    ax.add_collection(lc)

    # Add tile boundaries and annotations
    for t, (x, y, w, h) in tile_rects.items():
        rect = Rectangle((x, y), w, h, fill=False, edgecolor='red', linestyle='--', alpha=0.5)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, f'Tile {t}\n{tile_map.tiles[t].width}x{tile_map.tiles[t].height}', ha='center', va='center', fontsize=8)

    # Calculate proper plot limits
    all_x = [x for x, _, _, _ in tile_rects.values()]
    all_y = [y for _, y, _, _ in tile_rects.values()]
    min_x, max_x = min(all_x), max(x + w for x, _, w, _ in tile_rects.values())
    min_y, max_y = min(all_y), max(y + h for _, y, _, h in tile_rects.values())

    # Configure plot
    ax.set_xlim(min_x - 1, max_x + 1)
    ax.set_ylim(min_y - 1, max_y + 1)
    ax.set_aspect('equal')
    plt.xticks([])
    plt.yticks([])
    # ax.grid(True, which='both', linestyle=':', alpha=0.5)
    ax.set_title(f'Hilbert Curve Across Tiles, N = {tile_map.get_total_n()}, N_p = {np.unique(proc_mapping).size}', pad=20)

    plt.gca().invert_yaxis()

    if save_as:
        Path(save_as).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_as, bbox_inches='tight', dpi=dpi)
    if show:
        plt.show()

    return fig
