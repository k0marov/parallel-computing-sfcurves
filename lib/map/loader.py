import json
from dataclasses import dataclass
from typing import List
from pathlib import Path
from .map import TileDTO, NextConnect


@dataclass
class TileConfig:
    size: int
    connection: str


def load_tile_dtos(json_path: str | Path) -> List[TileDTO]:
    """
    Load tile configurations from JSON file and return list of TileDTOs

    Args:
        json_path: Path to JSON configuration file

    Returns:
        List of TileDTO objects

    Example JSON format:
    [
        {"width": 2, "height": 3, "connection": "RIGHT"},
        {"width": 4, "height": 5, "connection": "BOTTOM"}
    ]
    """
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"Tile config file not found: {path}")

    with open(path, 'r') as f:
        raw_configs = json.load(f)

    tile_dtos = []
    for config in raw_configs:
        try:
            connection = NextConnect[config['connection'].upper()]
            tile_dtos.append(
                TileDTO(width=config['width'], height=config['height'], next_conn=connection)
            )
        except KeyError as e:
            raise ValueError(f"Invalid connection type: {config['connection']}") from e
        except TypeError as e:
            raise ValueError("Invalid JSON structure") from e

    return tile_dtos