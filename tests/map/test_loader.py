import pytest
import json
from tempfile import NamedTemporaryFile
from pathlib import Path
from lib.map.loader import load_tile_dtos, TileConfig
from lib.map.map import NextConnect


def test_load_valid_config():
    """Test loading valid JSON configuration"""
    config = [
        {"width": 2, "height": 3, "connection": "RIGHT"},
        {"width": 4, "height": 5, "connection": "BOTTOM"}
    ]

    with NamedTemporaryFile('w', suffix='.json') as f:
        json.dump(config, f)
        f.flush()
        tiles = load_tile_dtos(f.name)

    assert len(tiles) == 2
    assert tiles[0].width == 2
    assert tiles[0].height == 3
    assert tiles[0].next_conn == NextConnect.RIGHT
    assert tiles[1].width == 4
    assert tiles[1].height == 5
    assert tiles[1].next_conn == NextConnect.BOTTOM


def test_invalid_connection_type():
    """Test invalid connection type in JSON"""
    config = [{"size": 2, "connection": "DIAGONAL"}]  # Invalid

    with NamedTemporaryFile('w', suffix='.json') as f:
        json.dump(config, f)
        f.flush()
        with pytest.raises(ValueError):
            load_tile_dtos(f.name)


def test_missing_file():
    """Test error when file doesn't exist"""
    with pytest.raises(FileNotFoundError):
        load_tile_dtos("nonexistent.json")


def test_invalid_json_structure():
    """Test malformed JSON file"""
    with NamedTemporaryFile('w', suffix='.json') as f:
        f.write("not valid json")
        f.flush()
        with pytest.raises(ValueError):
            load_tile_dtos(f.name)


def test_case_insensitive_connections():
    """Test connection type case insensitivity"""
    config = [{"width": 2, "height": 4, "connection": "right"}]  # Lowercase

    with NamedTemporaryFile('w', suffix='.json') as f:
        json.dump(config, f)
        f.flush()
        tiles = load_tile_dtos(f.name)

    assert tiles[0].next_conn == NextConnect.RIGHT