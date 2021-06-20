import numpy as np
import matplotlib.pyplot as plt

from utils.polygonCutter import PolygonCutter
from utils.polygonRequest import PolygonRequest

polygonRequest = PolygonRequest()
XTarget, YTarget, polygon = polygonRequest.getJsonInfo()

polygonCutter = PolygonCutter()
array_chm = polygonCutter.CutPolygonFromArrayGDALds(XTarget, YTarget, polygon)


#XTarget > XupperLeft and XTarget < XupperLeft+1000
#YTarget > YupperLeft-500 and YTarget < YupperLeft

col = 108
row = 105

# we create a grid where elevation data can map on
X = np.arange(row)
Y = np.arange(col)
X, Y = np.meshgrid(X, Y)


fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_surface(X, Y, array_chm, cmap='viridis', edgecolor='none')
# ax.plot_wireframe(X, Y, array_dtm, color='black')
ax.view_init(30,135)
# ax.set_zlim(6,13)
# ax.invert_zaxis()
plt.show()
