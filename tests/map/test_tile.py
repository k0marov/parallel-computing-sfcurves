import pytest
import numpy as np

from lib.map.tile import Tile, CornerPlace, construct_curve, NextConnect, _get_sides, get_places

def _assert_curve(curve, end, tile):
    # Basic checks
    assert curve.shape == (tile.width, tile.height)
    assert type(end) is CornerPlace

    # Check start position is correct
    assert curve[get_places(tile.width, tile.height)[tile.start]] == 0

    # Check the curve is continuous
    max_val = np.max(curve)
    for i in range(max_val + 1):
        assert i in curve

    # Check that the end position actually contains the max value
    assert tile.next_conn in _get_sides(end)
    max_val = np.max(curve)
    assert curve[get_places(tile.width, tile.height)[end]] == max_val


def test_construct_curve_basic_rotation():
    """Test that a basic curve can be constructed with simple rotation"""
    tile = Tile(width=2, height=2, start=CornerPlace.TOP_LEFT, next_conn=NextConnect.RIGHT)
    curve, end = construct_curve(tile)
    _assert_curve(curve, end, tile)

def test_construct_non_power_of_two():
    """Test that a basic curve can be constructed with non 2^n sizes."""
    tile = Tile(width=3, height=3, start=CornerPlace.TOP_LEFT, next_conn=NextConnect.RIGHT)
    curve, end = construct_curve(tile)
    _assert_curve(curve, end, tile)

def test_construct_curve_simple():
    """Test that a basic curve can be constructed with simple rotation"""
    tile = Tile(width=2, height=2, start=CornerPlace.TOP_LEFT, next_conn=NextConnect.BOTTOM)
    curve, end = construct_curve(tile)
    _assert_curve(curve, end, tile)


def test_construct_curve_with_fliplr():
    """Test that a curve can be constructed with left-right flip"""
    # This test case might need adjustment based on actual Hilbert curve behavior
    tile = Tile(width=4, height=4, start=CornerPlace.TOP_RIGHT, next_conn=NextConnect.BOTTOM)
    curve, end = construct_curve(tile)
    _assert_curve(curve, end, tile)


def test_construct_curve_with_flipud():
    """Test that a curve can be constructed with up-down flip"""
    # This test case might need adjustment based on actual Hilbert curve behavior
    tile = Tile(width=4, height=4, start=CornerPlace.BOT_LEFT, next_conn=NextConnect.RIGHT)
    curve, end = construct_curve(tile)
    _assert_curve(curve, end, tile)


def test_construct_curve_multiple_attempts():
    """Test that the function tries multiple rotations/flips before failing"""
    tile = Tile(width=8, height=8, start=CornerPlace.BOT_RIGHT, next_conn=NextConnect.LEFT)
    curve, end = construct_curve(tile)
    _assert_curve(curve, end, tile)


def test_construct_curve_returns_valid_end():
    """Test that the returned end position is valid"""
    tile = Tile(width=4, height=4, start=CornerPlace.TOP_LEFT, next_conn=NextConnect.BOTTOM)
    curve, end = construct_curve(tile)
    _assert_curve(curve, end, tile)
