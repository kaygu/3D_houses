from utils.handle_tiles import parse_geotiffs, split_tile, get_tile, check_tiff_files, clean_tiles

# {} = 'DTM' or 'DSM'
DATA_PATH = './data/{}/'
TILES_PATH = './data/{}_split/'


if __name__ == "__main__":
    # Check if all files needed exist before execution, then store every tiles info in DataFrame
    check_tiff_files()
    tiles = parse_geotiffs(path=DATA_PATH)

    # Main loop
    tile = get_tile(tiles, (218886.35, 220360.26))
    split_tile(tile, input=DATA_PATH, output=TILES_PATH)

    # Clean tile files after execution
    clean_tiles(tiles_path= TILES_PATH)
