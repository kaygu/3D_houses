from utils.polygonCutter import PolygonCutter
from utils.polygonRequest import PolygonRequest

polygonRequest = PolygonRequest()
XTarget, YTarget, polygon = polygonRequest.getJsonInfo()

polygonCutter = PolygonCutter()
array_chm = polygonCutter.CutPolygonFromArrayGDALds(XTarget, YTarget, polygon)


#XTarget > XupperLeft and XTarget < XupperLeft+1000
#YTarget > YupperLeft-500 and YTarget < YupperLeft
