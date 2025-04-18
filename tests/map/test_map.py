import pytest
import numpy as np
from lib.map.map import Map, TileDTO, NextConnect, CornerPlace
from lib.map.tile import get_places


@pytest.fixture
def basic_tile_dtos():
    return [
        TileDTO(width=2, height=2, next_conn=NextConnect.RIGHT),
        TileDTO(width=2, height=2, next_conn=NextConnect.BOTTOM),
        TileDTO(width=2, height=2, next_conn=NextConnect.LEFT)
    ]


def test_continuous_numbering_across_tiles(basic_tile_dtos):
    """Verify curve values are continuous across all tiles with correct offsets"""
    tile_map = Map(basic_tile_dtos)

    # Collect all values from all tiles
    all_values = np.concatenate([curve.flatten() for curve in tile_map.tile_curves])

    # Should contain all numbers from 0 to (total_points - 1)
    expected_values = set(range(tile_map.get_total_n()))
    actual_values = set(all_values)

    assert actual_values == expected_values, "Missing or duplicate indices in continuous curve"
    assert np.all(np.diff(np.sort(all_values)) == 1), "Curve numbering is not continuous"

def test_connection(basic_tile_dtos):
    """Verify that proper connection is applied."""
    tile_map = Map([TileDTO(width=2, height=2, next_conn=NextConnect.RIGHT), TileDTO(width=4, height=4, next_conn=NextConnect.BOTTOM)])
    assert tile_map.get_by_ind(3) == (0, 0, 1)
    assert tile_map.get_by_ind(19) == (1, 3, 0)

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
        TileDTO(width=4, height=4, next_conn=NextConnect.RIGHT),  # 16 points (0-15)
        TileDTO(width=2, height=2, next_conn=NextConnect.BOTTOM)  # 4 points (16-19)
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
    get_start = lambda i: get_places(tile_map.tiles[i].width, tile_map.tiles[i].height)[tile_map.tiles[i].start]

    assert tile_map.get_ind(0, *get_start(0)) == 0
    assert tile_map.get_ind(1, *get_start(1)) == 4
    assert tile_map.get_ind(2, *get_start(2)) == 8


def test_reverse_lookup_continuous(basic_tile_dtos):
    """Test coordinate lookup for all indices"""
    tile_map = Map(basic_tile_dtos)

    # Test every possible index
    for idx in range(tile_map.get_total_n()):
        t, x, y = tile_map.get_by_ind(idx)
        assert t >= 0 and x >= 0 and y >= 0, f"Failed lookup for index {idx}"
        assert tile_map.get_ind(t, x, y) == idx, f"Inconsistent mapping for {idx}"


def test_reverse_lookup_mixed_sizes():
    """Test with different tile sizes"""
    tile_dtos = [
        TileDTO(width=4, height=4, next_conn=NextConnect.RIGHT),
        TileDTO(width=4, height=4, next_conn=NextConnect.BOTTOM)
    ]
    tile_map = Map(tile_dtos)
    for i in range(6):
        assert tile_map.get_ind(*tile_map.get_by_ind(i)) == i
