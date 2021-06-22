import re
from utils.polygonCutter import PolygonCutter
from utils.polygonRequest import PolygonRequest
from utils.plotter import Plotter
from utils.handle_tiles import parse_geotiffs, split_tile, get_tile, check_tiff_files, clean_tiles

# {} = 'DTM' or 'DSM'
DATA_PATH = './data/{}/'
TILES_PATH = './data/{}_split/'


if __name__ == "__main__":
    # Check if all files needed exist before execution, then store every tiles info in DataFrame
    check_tiff_files()
    tiles = parse_geotiffs(path=DATA_PATH)

    polygonRequest = PolygonRequest()
    polygonCutter = PolygonCutter()

    # We do the request of the address of the building we want to visualize
    # Nollekensstraat 15 as default address located into the split tile 212

    print('Please enter the address of the building to plot...')
    while True:
        street = input('Street name: ')
        if re.match(r'^[a-zA-Z\s]+$', street):
            break
        print('Please enter a only letters street name')

    while True:
        number = input('Number: ')
        if re.match(r'^[0-9]+$', number):
            break
        print('Please enter only numbers')

    while True:
        postalCode = input('PostalCode: ')
        if re.match(r'^[0-9]+$', postalCode):
            break
        print('Please enter only numbers')

    while True:
        comune = input('Comune: ')
        if re.match(r'^[a-zA-Z\s]+$', comune):
            break
        print('Please enter only numbers')


    XTarget, YTarget, polygon = polygonRequest.getJsonInfo(street, number, postalCode, comune)

    # XTarget, YTarget, polygon = polygonRequest.getJsonInfo(street='Schoenmarkt', houseNumb='35')

    # We get the tile corresponding to the coordinates
    tile = get_tile(tiles, (XTarget, YTarget))
    split_tile(tile, input=DATA_PATH, output=TILES_PATH)

    # Now we gate the CHM array corresponding at the polygon and the tile number
    array_chm = polygonCutter.CutPolygonFromArrayGDALds(polygon, tile.name)

    # Clean tile files after execution
    clean_tiles(tiles_path= TILES_PATH)

    # plot chm
    plotter = Plotter(array_chm)
    plotter.createPlot()

