import os
import pandas as pd
from osgeo import gdal
from threading import Thread
from typing import List, Dict, Union


class SplitGeoTiff(Thread):
    '''Split big geoTIFFs files in shorter ones. Folders must be unziped first'''
    def __init__(self, type: str = 'DSM', nb_files: int = 43, input: str = './data/{}/', output: str = './data/{}_split/'):
        Thread.__init__(self)
        self.type: str = type
        self.in_path: str = f"{input.format(type)}/DHMVII{type}RAS1m_k"
        self.in_file: str = f"DHMVII{type}RAS1m_k"
        self.out_path: str = output.format(type)
        self.out_file: str = "tile_"
        self.nb_files: int = nb_files + 1
        self.tiles: Dict[str, Union[List[int], List[float]]] = {'tile': [], 'X': [], 'Y': []}

    def run(self):
        cpt=0
        for x in range(1, self.nb_files):
            if x < 10:
                tile = f"0{x}"
            else :
                tile = str(x)
            print(f"Getting {self.type} map n°{tile}, total tiles : {cpt}")   


            in_path = self.in_path + tile + '/GeoTIFF/'
            in_file = self.in_file + tile + ".tif"

            tile_size_x = 1000
            tile_size_y = 500

            ds = gdal.Open(in_path + in_file)
            coords = ds.GetGeoTransform()
            band = ds.GetRasterBand(1)
            xsize = band.XSize
            ysize = band.YSize
            for i in range(0, xsize, tile_size_x):
                for j in range(0, ysize, tile_size_y):
                    cpt += 1
                    self.tiles['tile'].append(cpt)
                    self.tiles['X'].append(coords[0] + i)
                    self.tiles['Y'].append(coords[3] - j)
                    cmd_str = f'gdal_translate -of GTIFF -srcwin {i}, {j}, {tile_size_x}, {tile_size_y} {in_path + in_file} {self.out_path + self.out_file + str(cpt)}.tif > logs_{self.type}.log'
                    os.system(cmd_str)

