import pytest
import numpy as np
from lib.map.map import Map, TileDTO, NextConnect, CornerPlace
from lib.map.tile import get_places


@pytest.fixture
def basic_tile_dtos():
    return [
        TileDTO(n=2, next_conn=NextConnect.RIGHT),
        TileDTO(n=2, next_conn=NextConnect.BOTTOM),
        TileDTO(n=2, next_conn=NextConnect.LEFT)
    ]


def test_continuous_numbering_across_tiles(basic_tile_dtos):
    """Verify curve values are continuous across all tiles with correct offsets"""
    tile_map = Map(basic_tile_dtos)

    # Collect all values from all tiles
    all_values = np.concatenate([curve.flatten() for curve in tile_map.tile_curves])

    # Should contain all numbers from 0 to (total_points - 1)
    total_points = sum(tile.n ** 2 for tile in basic_tile_dtos)
    expected_values = set(range(total_points))
    actual_values = set(all_values)

    assert actual_values == expected_values, "Missing or duplicate indices in continuous curve"
    assert np.all(np.diff(np.sort(all_values)) == 1), "Curve numbering is not continuous"


def test_correct_offsets_applied(basic_tile_dtos):
    """Verify each tile's curve has the correct offset applied"""
    tile_map = Map(basic_tile_dtos)

    # First tile (2x2) should have values 0-3
    assert np.min(tile_map.tile_curves[0]) == 0
    assert np.max(tile_map.tile_curves[0]) == 3

    # Second tile (2x2) should have values 4-7
    assert np.min(tile_map.tile_curves[1]) == 4
    assert np.max(tile_map.tile_curves[1]) == 7

    # Third tile (2x2) should have values 8-11
    assert np.min(tile_map.tile_curves[2]) == 8
    assert np.max(tile_map.tile_curves[2]) == 11


def test_mixed_tile_sizes():
    """Test with tiles of different sizes"""
    tile_dtos = [
        TileDTO(n=4, next_conn=NextConnect.RIGHT),  # 16 points (0-15)
        TileDTO(n=2, next_conn=NextConnect.BOTTOM)  # 4 points (16-19)
    ]
    tile_map = Map(tile_dtos)

    # Verify first tile offset
    assert np.min(tile_map.tile_curves[0]) == 0
    assert np.max(tile_map.tile_curves[0]) == 15

    # Verify second tile offset
    assert np.min(tile_map.tile_curves[1]) == 16
    assert np.max(tile_map.tile_curves[1]) == 19

    # Verify full continuity
    all_values = np.concatenate([curve.flatten() for curve in tile_map.tile_curves])
    assert set(all_values) == set(range(20)), "Missing values in mixed-size map"


def test_get_ind_returns_correct_values(basic_tile_dtos):
    """Verify get_ind returns the correct continuous index"""
    tile_map = Map(basic_tile_dtos)

    # Test indices across tile boundaries
    get_start = lambda i: get_places(tile_map.tiles[i].n, tile_map.tiles[i].n)[tile_map.tiles[i].start]

    assert tile_map.get_ind(0, *get_start(0)) == 0
    assert tile_map.get_ind(1, *get_start(1)) == 4
    assert tile_map.get_ind(2, *get_start(2)) == 8