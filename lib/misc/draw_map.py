# lib/map/visualization.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import Rectangle
from typing import Optional, Tuple
from pathlib import Path

from lib.map.map import Map
from lib.map.tile import NextConnect


def calculate_tile_positions(tile_map: Map) -> Tuple[dict, dict]:
    """
    Calculate proper tile positions with normalized sizes.
    Returns:
        - tile_positions: Dict of {tile_index: (x, y)} for tile origins
        - tile_rects: Dict of {tile_index: (x, y, width, height)} with normalized sizes
    """
    tile_positions = {}
    tile_rects = {}
    current_x, current_y = 0, 0

    # Define fixed tile size for visualization
    TILE_SIZE = 1.0
    TILE_MARGIN = 0.05

    for t, tile in enumerate(tile_map.tiles):
        # Store tile position with fixed size
        tile_positions[t] = (current_x, current_y)
        tile_rects[t] = (current_x, current_y, TILE_SIZE, TILE_SIZE)

        # Calculate position for next tile based on connection
        if t < len(tile_map.tiles) - 1:
            next_conn = tile.next_conn
            if next_conn == NextConnect.RIGHT:
                current_x += TILE_SIZE + TILE_MARGIN
            elif next_conn == NextConnect.LEFT:
                current_x -= TILE_SIZE + TILE_MARGIN
            elif next_conn == NextConnect.TOP:
                current_y += TILE_SIZE + TILE_MARGIN
            elif next_conn == NextConnect.BOTTOM:
                current_y -= TILE_SIZE + TILE_MARGIN

    return tile_positions, tile_rects


def create_repeating_tab20_colormap(n_colors):
    """Create a colormap that repeats tab20 colors when n_colors > 20"""
    # Get the base tab20 colors
    tab20_colors = plt.cm.tab20.colors
    base_colors = list(tab20_colors)
    
    if n_colors <= 20:
        return plt.cm.colors.ListedColormap(base_colors[:n_colors])
    else:
        # Repeat the colors until we have enough
        repeated_colors = []
        for i in range(n_colors):
            repeated_colors.append(base_colors[i % 20])
        return plt.cm.colors.ListedColormap(repeated_colors)


def visualize_map_lines(tile_map: Map,
                       proc_mapping: np.array,
                       save_as: Optional[str] = None,
                       show: bool = True,
                       dpi: int = 100,
                       linewidth: float = 2.0,
                       figsize: Tuple[int, int] = (12, 10),
                       colormap: str = 'tab20') -> plt.Figure:
    """
    Visualization of the complete Hilbert curve using line segments (original working version).
    
    Args:
        tile_map: Initialized Map object
        proc_mapping: Mapping of hilbert index to processor
        save_as: Path to save the visualization
        show: Whether to display the plot
        dpi: Image resolution
        linewidth: Width of curve lines
        figsize: Figure dimensions in inches
        colormap: Colormap name
        
    Returns:
        matplotlib Figure object
    """
    # Calculate tile positions
    tile_positions, tile_rects = calculate_tile_positions(tile_map)
    
    # Create base_coords exactly as in the original working version
    base_coords = np.zeros((tile_map.get_total_n(), 2))
    for t, curve in enumerate(tile_map.tile_curves):
        tile_x, tile_y = tile_positions[t]
        width = tile_map.tiles[t].width
        height = tile_map.tiles[t].height
        
        # Calculate scaling to fit within the fixed tile size
        x_scale = 1.0 / max(1, width - 1) if width > 1 else 0
        y_scale = 1.0 / max(1, height - 1) if height > 1 else 0
        
        for x in range(width):
            for y in range(height):
                hilbert_idx = curve[y, x]
                # Use the same coordinate calculation as original working version
                x_coord = tile_x + (x * x_scale) if width > 1 else tile_x + 0.5
                y_coord = tile_y + ((height - 1 - y) * y_scale) if height > 1 else tile_y + 0.5
                base_coords[hilbert_idx] = [x_coord, y_coord]

    # Create line segments for the entire curve (original working logic)
    segments = np.array([base_coords[:-1], base_coords[1:]]).transpose(1, 0, 2)
    segment_values = proc_mapping[1:]  # Color by the target point of each segment
    
    # Get unique processors and create colormap
    unique_processors = np.unique(proc_mapping)
    num_processors = len(unique_processors)
    
    # Create the appropriate colormap
    if colormap == 'tab20':
        cmap_discrete = create_repeating_tab20_colormap(num_processors)
    else:
        cmap = plt.get_cmap(colormap)
        if num_processors <= 20 and colormap in ['tab20', 'tab20b', 'tab20c']:
            colors = cmap(np.linspace(0, 1, max(20, num_processors)))[:num_processors]
            cmap_discrete = plt.cm.colors.ListedColormap(colors)
        else:
            colors = cmap(np.linspace(0, 1, num_processors))
            cmap_discrete = plt.cm.colors.ListedColormap(colors)
    
    # Create normalization
    norm = plt.Normalize(vmin=unique_processors.min(), vmax=unique_processors.max())
    segment_colors = cmap_discrete(norm(segment_values))

    # Create figure and plot
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    lc = LineCollection(segments, linewidth=linewidth, colors=segment_colors)
    ax.add_collection(lc)

    # Add tile boundaries and annotations
    for t, (x, y, w, h) in tile_rects.items():
        rect = Rectangle((x, y), w, h, fill=False, edgecolor='red', 
                        linestyle='--', alpha=0.7, linewidth=1.5)
        ax.add_patch(rect)
        
        tile = tile_map.tiles[t]
        ax.text(x + w / 2, y + h / 2, 
                f'Tile {t}\n{tile.width}x{tile.height}', 
                ha='center', va='center', fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    # Calculate proper plot limits
    all_x = [x for x, _, _, _ in tile_rects.values()]
    all_y = [y for _, y, _, _ in tile_rects.values()]
    min_x, max_x = min(all_x), max(x + w for x, _, w, _ in tile_rects.values())
    min_y, max_y = min(all_y), max(y + h for _, y, _, h in tile_rects.values())
    
    # Add padding
    padding = 0.5
    ax.set_xlim(min_x - padding, max_x + padding)
    ax.set_ylim(min_y - padding, max_y + padding)
    
    ax.set_aspect('equal')
    plt.xticks([])
    plt.yticks([])
    
    total_points = tile_map.get_total_n()
    ax.set_title(f'Hilbert Curve (Line Segments)\nTotal Points: {total_points}, Processors: {num_processors}', 
                 pad=20, fontsize=14)

    if save_as:
        Path(save_as).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_as, bbox_inches='tight', dpi=dpi)
    if show:
        plt.show()

    return fig


def visualize_map_rectangles(tile_map: Map,
                            proc_mapping: np.array,
                            save_as: Optional[str] = None,
                            show: bool = True,
                            dpi: int = 100,
                            figsize: Tuple[int, int] = (12, 10),
                            colormap: str = 'tab20') -> plt.Figure:
    """
    Visualization of the complete Hilbert curve as colored rectangles filling each tile.
    """
    # Calculate tile positions
    tile_positions, tile_rects = calculate_tile_positions(tile_map)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    # Get the unique processor IDs
    unique_processors = np.unique(proc_mapping)
    num_processors = len(unique_processors)
    
    # Create the appropriate colormap
    if colormap == 'tab20':
        cmap_discrete = create_repeating_tab20_colormap(num_processors)
    else:
        cmap = plt.get_cmap(colormap)
        if num_processors <= 20 and colormap in ['tab20', 'tab20b', 'tab20c']:
            colors = cmap(np.linspace(0, 1, max(20, num_processors)))[:num_processors]
            cmap_discrete = plt.cm.colors.ListedColormap(colors)
        else:
            colors = cmap(np.linspace(0, 1, num_processors))
            cmap_discrete = plt.cm.colors.ListedColormap(colors)
    
    # Create normalization
    norm = plt.Normalize(vmin=unique_processors.min(), vmax=unique_processors.max())
    
    # Create rectangles for each cell
    from matplotlib.patches import Rectangle
    from matplotlib.collections import PatchCollection
    
    patches = []
    colors_list = []
    
    for t, curve in enumerate(tile_map.tile_curves):
        tile_x, tile_y = tile_positions[t]
        width = tile_map.tiles[t].width
        height = tile_map.tiles[t].height
        
        # Calculate cell size within the tile
        cell_width = 1.0 / width
        cell_height = 1.0 / height
        
        for x in range(width):
            for y in range(height):
                hilbert_idx = curve[y, x]
                
                # Get the processor ID using the same logic as line version
                processor_id = proc_mapping[hilbert_idx]
                
                # Calculate cell position
                cell_x = tile_x + x * cell_width
                cell_y = tile_y + (height - 1 - y) * cell_height
                
                # Create rectangle for this cell
                rect = Rectangle((cell_x, cell_y), cell_width, cell_height)
                patches.append(rect)
                
                # Get color using the same colormap logic
                color = cmap_discrete(norm(processor_id))
                colors_list.append(color)

    # Create patch collection
    pc = PatchCollection(patches, facecolor=colors_list, edgecolor='white', 
                         linewidth=0.3, alpha=0.95)
    ax.add_collection(pc)

    # Add tile boundaries
    for t, (x, y, w, h) in tile_rects.items():
        rect = Rectangle((x, y), w, h, fill=False, edgecolor='black', 
                        linestyle='-', alpha=0.8, linewidth=2)
        ax.add_patch(rect)
        
        # Add tile annotation
        tile = tile_map.tiles[t]
        ax.text(x + w / 2, y + h / 2, 
                f'Tile {t}\n{tile.width}x{tile.height}', 
                ha='center', va='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))

    # Calculate proper plot limits with some padding
    all_x = [x for x, _, _, _ in tile_rects.values()]
    all_y = [y for _, y, _, _ in tile_rects.values()]
    min_x, max_x = min(all_x), max(x + w for x, _, w, _ in tile_rects.values())
    min_y, max_y = min(all_y), max(y + h for _, y, _, h in tile_rects.values())
    
    # Add padding
    padding = 0.3
    ax.set_xlim(min_x - padding, max_x + padding)
    ax.set_ylim(min_y - padding, max_y + padding)
    
    ax.set_aspect('equal')
    plt.xticks([])
    plt.yticks([])
    
    total_points = tile_map.get_total_n()
    ax.set_title(f'Hilbert Curve (Rectangles)\nTotal Cells: {total_points}, Processors: {num_processors}', 
                 pad=20, fontsize=14)
    
    plt.tight_layout()

    if save_as:
        Path(save_as).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_as, bbox_inches='tight', dpi=dpi, facecolor='white')
    if show:
        plt.show()

    return fig


def visualize_both(tile_map: Map,
                  proc_mapping: np.array,
                  save_as: Optional[str] = None,
                  show: bool = True,
                  dpi: int = 100,
                  figsize: Tuple[int, int] = (20, 8)) -> plt.Figure:
    """
    Visualize both line segments and rectangles side by side for comparison.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, dpi=dpi)
    
    # First subplot: Line segments
    tile_positions, tile_rects = calculate_tile_positions(tile_map)
    
    # Create base_coords for line segments
    base_coords = np.zeros((tile_map.get_total_n(), 2))
    for t, curve in enumerate(tile_map.tile_curves):
        tile_x, tile_y = tile_positions[t]
        width = tile_map.tiles[t].width
        height = tile_map.tiles[t].height
        
        x_scale = 1.0 / max(1, width - 1) if width > 1 else 0
        y_scale = 1.0 / max(1, height - 1) if height > 1 else 0
        
        for x in range(width):
            for y in range(height):
                hilbert_idx = curve[y, x]
                x_coord = tile_x + (x * x_scale) if width > 1 else tile_x + 0.5
                y_coord = tile_y + ((height - 1 - y) * y_scale) if height > 1 else tile_y + 0.5
                base_coords[hilbert_idx] = [x_coord, y_coord]

    segments = np.array([base_coords[:-1], base_coords[1:]]).transpose(1, 0, 2)
    segment_values = proc_mapping[1:]
    
    unique_processors = np.unique(proc_mapping)
    cmap_discrete = create_repeating_tab20_colormap(len(unique_processors))
    norm = plt.Normalize(vmin=unique_processors.min(), vmax=unique_processors.max())
    segment_colors = cmap_discrete(norm(segment_values))

    lc = LineCollection(segments, linewidth=2, colors=segment_colors)
    ax1.add_collection(lc)
    
    # Add tile boundaries
    for t, (x, y, w, h) in tile_rects.items():
        rect = Rectangle((x, y), w, h, fill=False, edgecolor='red', linestyle='--', alpha=0.7)
        ax1.add_patch(rect)
    
    ax1.set_xlim(-0.5, max(x + w for x, _, w, _ in tile_rects.values()) + 0.5)
    ax1.set_ylim(-0.5, max(y + h for _, y, _, h in tile_rects.values()) + 0.5)
    ax1.set_aspect('equal')
    ax1.set_title('Line Segments', fontsize=14)
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    # Second subplot: Rectangles
    patches = []
    colors_list = []
    
    for t, curve in enumerate(tile_map.tile_curves):
        tile_x, tile_y = tile_positions[t]
        width = tile_map.tiles[t].width
        height = tile_map.tiles[t].height
        cell_width = 1.0 / width
        cell_height = 1.0 / height
        
        for x in range(width):
            for y in range(height):
                hilbert_idx = curve[y, x]
                processor_id = proc_mapping[hilbert_idx]
                cell_x = tile_x + x * cell_width
                cell_y = tile_y + (height - 1 - y) * cell_height
                
                rect = Rectangle((cell_x, cell_y), cell_width, cell_height)
                patches.append(rect)
                colors_list.append(cmap_discrete(norm(processor_id)))
    
    pc = PatchCollection(patches, facecolor=colors_list, edgecolor='white', linewidth=0.2, alpha=0.95)
    ax2.add_collection(pc)
    
    # Add tile boundaries
    for t, (x, y, w, h) in tile_rects.items():
        rect = Rectangle((x, y), w, h, fill=False, edgecolor='black', linestyle='-', alpha=0.8, linewidth=2)
        ax2.add_patch(rect)
    
    ax2.set_xlim(-0.5, max(x + w for x, _, w, _ in tile_rects.values()) + 0.5)
    ax2.set_ylim(-0.5, max(y + h for _, y, _, h in tile_rects.values()) + 0.5)
    ax2.set_aspect('equal')
    ax2.set_title('Rectangles', fontsize=14)
    ax2.set_xticks([])
    ax2.set_yticks([])
    
    plt.suptitle(f'Hilbert Curve Visualization Comparison\nTotal Points: {tile_map.get_total_n()}, Processors: {len(unique_processors)}', 
                 fontsize=16)
    plt.tight_layout()
    
    if save_as:
        Path(save_as).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_as, bbox_inches='tight', dpi=dpi, facecolor='white')
    if show:
        plt.show()

    return fig