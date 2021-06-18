from utils.polygonCutter import PolygonCutter
from utils.polygonRequest import PolygonRequest

polygonRequest = PolygonRequest()
XTarget, YTarget, polygon = polygonRequest.getJsonInfo()
#XTarget, YTarget, polygon = polygonRequest.getJsonInfo(street='Schoenmarkt', houseNumb='35')

polygonCutter = PolygonCutter()

# This function get the tile number
tileNumber = polygonCutter.getTileNumber(XTarget, YTarget)
print(tileNumber)
array_chm = polygonCutter.CutPolygonFromArrayGDALds(polygon, tileNumber)


