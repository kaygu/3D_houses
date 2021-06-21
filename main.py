from utils.polygonCutter import PolygonCutter
from utils.polygonRequest import PolygonRequest
from utils.handle_tiles import parse_geotiffs, split_tile, get_tile, check_tiff_files, clean_tiles

# {} = 'DTM' or 'DSM'
DATA_PATH = './data/{}/'
TILES_PATH = './data/{}_split/'


if __name__ == "__main__":
    # Check if all files needed exist before execution, then store every tiles info in DataFrame
    check_tiff_files()
    tiles = parse_geotiffs(path=DATA_PATH)

    polygonRequest = PolygonRequest()
    XTarget, YTarget, polygon = polygonRequest.getJsonInfo()
    # XTarget, YTarget, polygon = polygonRequest.getJsonInfo(street='Schoenmarkt', houseNumb='35')

    polygonCutter = PolygonCutter()

    # Main loop
    tile = get_tile(tiles, (XTarget, YTarget))
    split_tile(tile, input=DATA_PATH, output=TILES_PATH)

    polygonCutter = PolygonCutter()

    # This function get the tile number
    #tileNumber = polygonCutter.getTileNumber(XTarget, YTarget)
    array_chm = polygonCutter.CutPolygonFromArrayGDALds(polygon, tile.name)

    # Clean tile files after execution
    clean_tiles(tiles_path= TILES_PATH)