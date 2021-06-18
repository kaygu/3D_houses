import pandas as pd
from utils.split_geotiffs import parse_geotiffs, split_tiles

# {} = 'DTM' or 'DSM'
INPUT_PATH = './data/{}/'
OUTPUT_PATH = './data/{}_split/'


if __name__ == "__main__":
    tiles = parse_geotiffs(input_path=INPUT_PATH)
    split_tiles(tiles.loc[555], input=INPUT_PATH, output=OUTPUT_PATH)

