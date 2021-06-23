import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from osgeo import gdal
from typing import Dict, List


class PolygonCutter:
    def __init__(self, tile_path: str = './data/{}_split/'):
        self.tile_path: str = tile_path
        self.flagPlots = True

    def CutPolygonFromArrayGDALds(self, polygon: Dict, tileNumber: int) -> np.ndarray:
        """
        This method gets the need tiles to calculate the chm, make the binary
        mask and get only and array with the data of only the desired building
        and return it
        :param polygon: This is a dictionary that contains the polygon of the building
        :param tileNumber: This is the number fo the tile we need to get the CHM
        :return: array with the data of the calculated CHM for the building
        """

        # We call the function which will give us the necessary CHM and limits info
        XupperLeft, YupperLeft, array_chm = self.getCHMFromGDAL(tileNumber, self.tile_path)

        # We create a new list of coordinates from our polygon
        xx = [i[0] - XupperLeft for i in polygon['coordinates'][0][:]]
        yy = [YupperLeft - i[1] for i in polygon['coordinates'][0][:]]

        coordinates = list(zip(xx, yy))

        # We create a binary mask based on the polygon
        maskIm = Image.new('L', (array_chm.shape[1], array_chm.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(coordinates, outline=1, fill=1)
        mask = np.array(maskIm)

        # Then we filter our CHM based on the binary mask
        array_chm_cut = np.where((mask == 1), array_chm, 0)

        # Resize the function cutting the array at the the size of the polygon
        array_chm = self.resizeMaskedArray(array_chm_cut)

        if self.flagPlots:
            plt.figure(5)
            plt.imshow(mask)
            plt.title('Binary Mask')

            plt.figure(6)
            plt.imshow(array_chm)
            plt.title('CHM Filtered and cut for the desired building')

        return array_chm

    def getCHMFromGDAL(self, tileNumber: int, tile_path: str = './data/{}_split/'):
        """
        This method open the respective tif to the tile Number and return the
        CHM array with the respective Upper Left Lambert coordinates

        :param tileNumber: It's the number of the tile were the building is
        located. Calculated by handle.tiles.get_tile
        :param tile_path: Set folder path for the tile files
        :return: CHM array with the respective Upper Left Lambert coordinates
        """
        # We open the respective tif files
        print('Opening tiles DSM and DTM number:', tileNumber)
        ds_dsm = gdal.Open(f'{tile_path.format("DSM")}tile_{str(tileNumber)}.tif')
        ds_dtm = gdal.Open(f'{tile_path.format("DTM")}tile_{str(tileNumber)}.tif')

        # Reading the bands as matrices
        array_dsm = ds_dsm.GetRasterBand(1).ReadAsArray().astype(np.float32)
        array_dtm = ds_dtm.GetRasterBand(1).ReadAsArray().astype(np.float32)

        # Getting the geotransformations
        gt_dsm = ds_dsm.GetGeoTransform()
        gt_dtm = ds_dtm.GetGeoTransform()

        XupperLeft, pixelWE, empty, YupperLeft, pixelNS, empty2 = gt_dsm

        # We create the canopy height model subtracting the other two
        array_chm = array_dsm - array_dtm

        if self.flagPlots:
            plt.figure(2)
            plt.imshow(array_dtm)
            plt.title('Digital Terrain Model')

            plt.figure(3)
            plt.imshow(array_dsm)
            plt.title('Digital Surface Model')

            plt.figure(4)
            plt.imshow(array_chm)
            plt.title('Canopy Height Model')

        return XupperLeft, YupperLeft, array_chm

    @staticmethod
    def resizeMaskedArray(array_chm_cut: np.ndarray):
        """
        This method resize the numpy array by deleting all the empty
        columns and rows

        :param array_chm_cut: CHM numpy array filtered with mask
        :return: cut CHM numpy array
        """
        data = array_chm_cut[~np.all(array_chm_cut == 0, axis=1)]
        idx = np.argwhere(np.all(data[..., :] == 0, axis=0))
        return np.delete(data, idx, axis=1)
