from lib import distribute
from lib.map.loader import load_tile_dtos
from lib.map.map import Map
from lib.misc.draw_map import visualize_map

# Load configuration
tile_dtos = load_tile_dtos("config.json")

# Create map
tile_map = Map(tile_dtos)
print(tile_map.tile_curves)

proc_mapping = distribute.split_into_processors(sum(t.n**2 for t in tile_dtos), 8)

# Visualize
visualize_map(tile_map,
              proc_mapping,
             save_as="hilbert_map.png",
             show=True,
             linewidth=2.0,
             figsize=(12, 8))