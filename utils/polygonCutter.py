import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from osgeo import gdal

class PolygonCutter:

    def CutPolygonFromArrayGDALds(self, XTarget, YTarget, polygon):

        XupperLeft, YupperLeft, array_chm = self.getCHMfromGDAL()
        xx = [i[0] - XupperLeft for i in polygon['coordinates'][0][:]]
        yy = [YupperLeft - i[1] for i in polygon['coordinates'][0][:]]

        coordinates = list(zip(xx, yy))

        maskIm = Image.new('L', (array_chm.shape[1], array_chm.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(coordinates, outline=1, fill=1)
        mask = np.array(maskIm)

        #black = Image.new('L', (array_chm.shape[1], array_chm.shape[0]), 0)
        #result = Image.composite(array_chm, black, mask)

        array_chm_cut = np.where((mask == 1), array_chm, 0)

        array_chm = self.resizeMaskedArray(array_chm_cut)

        plt.figure()
        plt.imshow(mask)
        plt.show()

        plt.figure()
        plt.imshow(array_chm)
        plt.show()

        return array_chm


    def getCHMfromGDAL(self, DSM_tile='assets/DSM_split/tile_212.tif', DTM_tile='assets/DTM_split/tile_212.tif'):
        ds_dsm = gdal.Open(DSM_tile)
        ds_dtm = gdal.Open(DTM_tile)

        # Reading the bands as matrices
        array_dsm = ds_dsm.GetRasterBand(1).ReadAsArray().astype(np.float32)
        array_dtm = ds_dtm.GetRasterBand(1).ReadAsArray().astype(np.float32)
        plt.figure()
        plt.imshow(array_dtm)
        plt.show()
        plt.figure()
        plt.imshow(array_dsm)
        plt.show()
        # Getting the geotransformations
        gt_dsm = ds_dsm.GetGeoTransform()
        gt_dtm = ds_dtm.GetGeoTransform()

        XupperLeft, pixelWE, empty, YupperLeft, pixelNS, empty2 = gt_dsm

        # We create the canopy height model subtracting the other two
        array_chm = array_dsm - array_dtm

        # array_chm = np.where((array_chm >=np.mean(array_chm)), array_dsm, 0)
        plt.figure()
        plt.imshow(array_chm)
        plt.show()

        return XupperLeft, YupperLeft, array_chm

    def resizeMaskedArray(self, array_chm_cut):
        data = array_chm_cut[~np.all(array_chm_cut == 0, axis=1)]
        idx = np.argwhere(np.all(data[..., :] == 0, axis=0))
        return np.delete(data, idx, axis=1)