from utils.polygonCutter import PolygonCutter
from utils.polygonRequest import PolygonRequest
from utils.plotter import Plotter

polygonRequest = PolygonRequest()
XTarget, YTarget, polygon = polygonRequest.getJsonInfo()
#XTarget, YTarget, polygon = polygonRequest.getJsonInfo(street='Schoenmarkt', houseNumb='35')

polygonCutter = PolygonCutter()

# This function get the tile number
#tileNumber = polygonCutter.ge.tTileNumber(XTarget, YTarget)
tileNumber = 212
print(tileNumber)
array_chm = polygonCutter.CutPolygonFromArrayGDALds(polygon, tileNumber)

plotter = Plotter(array_chm)
plotter.createPlot()

# createPlot(array_chm)