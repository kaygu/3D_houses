import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from osgeo import gdal


class PolygonCutter:

    def CutPolygonFromArrayGDALds(self, polygon, tileNumber):
        XupperLeft, YupperLeft, array_chm = self.getCHMfromGDAL(tileNumber)
        xx = [i[0] - XupperLeft for i in polygon['coordinates'][0][:]]
        yy = [YupperLeft - i[1] for i in polygon['coordinates'][0][:]]

        coordinates = list(zip(xx, yy))

        maskIm = Image.new('L', (array_chm.shape[1], array_chm.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(coordinates, outline=1, fill=1)
        mask = np.array(maskIm)

        array_chm_cut = np.where((mask == 1), array_chm, 0)

        array_chm = self.resizeMaskedArray(array_chm_cut)

        plt.figure()
        plt.imshow(mask)
        plt.title('Binary Mask')
        plt.show()

        plt.figure()
        plt.imshow(array_chm)
        plt.title('CHM Filtered and cut for the desired building')
        plt.show()

        return array_chm

    @staticmethod
    def getCHMfromGDAL(tileNumber=212):
        print('Opening tiles DSM and DTM number:', tileNumber)
        ds_dsm = gdal.Open('assets/DSM_split/tile_' + str(tileNumber) + '.tif')
        ds_dtm = gdal.Open('assets/DTM_split/tile_' + str(tileNumber) + '.tif')

        # Reading the bands as matrices
        array_dsm = ds_dsm.GetRasterBand(1).ReadAsArray().astype(np.float32)
        array_dtm = ds_dtm.GetRasterBand(1).ReadAsArray().astype(np.float32)
        plt.figure()
        plt.imshow(array_dtm)
        plt.title('Digital Terrain Model')
        plt.show()
        plt.figure()
        plt.imshow(array_dsm)
        plt.title('Digital Surface Model')
        plt.show()
        # Getting the geotransformations
        gt_dsm = ds_dsm.GetGeoTransform()
        gt_dtm = ds_dtm.GetGeoTransform()

        XupperLeft, pixelWE, empty, YupperLeft, pixelNS, empty2 = gt_dsm

        # We create the canopy height model subtracting the other two
        array_chm = array_dsm - array_dtm

        plt.figure()
        plt.imshow(array_chm)
        plt.title('Canopy Height Model')
        plt.show()

        return XupperLeft, YupperLeft, array_chm

    @staticmethod
    def resizeMaskedArray(array_chm_cut):
        data = array_chm_cut[~np.all(array_chm_cut == 0, axis=1)]
        idx = np.argwhere(np.all(data[..., :] == 0, axis=0))
        return np.delete(data, idx, axis=1)

    @staticmethod
    def getTileNumber(XTarget, YTarget):
        tiles = pd.read_csv('assets/tiles.csv')
        tile = tiles[(XTarget > tiles['X']) & (XTarget < tiles['X'] + 1000)]
        tile = tile[(YTarget > tile['Y'] - 500) & (YTarget < tile['Y'])]
        return tile['tile'].iloc[0]
