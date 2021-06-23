from utils.polygonCutter import PolygonCutter
from utils.polygonRequest import PolygonRequest
from utils.plotter import Plotter
from utils.TileManager import TileManager

# {} = 'DTM' or 'DSM'
DATA_PATH = './data/{}/'
TILES_PATH = './data/{}_split/'


if __name__ == "__main__":
    # Instantiate classes
    tileManager = TileManager(DATA_PATH, TILES_PATH)
    polygonRequest = PolygonRequest()
    polygonCutter = PolygonCutter(TILES_PATH)

    # Check if all files needed exist before execution, then store every tiles info in DataFrame
    tileManager.check_tiff_files()
    tiles = tileManager.parse_geotiffs()

    XTarget, YTarget, polygon, flagPlots = polygonRequest.getJsonInfo()

    # We get the tile corresponding to the coordinates
    tile = tileManager.get_tile(tiles, (XTarget, YTarget))
    tileManager.split_tile(tile)
    
    polygonCutter.flagPlots = flagPlots

    # Now we gate the CHM array corresponding at the polygon and the tile number
    array_chm = polygonCutter.CutPolygonFromArrayGDALds(polygon, tile.name)

    # Plot Canopy Height Model
    plotter = Plotter(array_chm)
    plotter.createPlot(polygonRequest.address)

    # Clean tile files after execution
    tileManager.clean_tiles()