import os
from osgeo import gdal
import pandas as pd
import re
from typing import List, Dict, Union, Tuple


class TileManager:
    def __init__(self, data_path: str = './data/{}/', tile_path: str = './data/{}_split/'):
        self.data_path = data_path
        self.tile_path = tile_path
        self.csv_name = 'tiles.csv'

    def parse_geotiffs(self) -> pd.DataFrame:
        """
        Cycle through every DTM tif files to count how much tiles you have in total
        :param path: Path where your data is stored. './data/{}/' by default.
        :return: dataframe containing all the tiles available
        """
        input_path = self.data_path.format('DTM')
        tiles: Dict[str, Union[List[int], List[float], Tuple[int, int]]] = {
            'tile_nb': [],
            'X': [],
            'Y': [],
            'origin_file': [],
            'img_pos': [],
            'img_size': []}
        dirs = os.listdir(input_path)
        count = 0
        tile_size_x = 1000
        tile_size_y = 500
        for file in dirs:
            try:
                ds = gdal.Open(f'{input_path}{file}/GeoTIFF/{file}.tif')
                coords = ds.GetGeoTransform()
                band = ds.GetRasterBand(1)
            except:
                print(f"Something went wrong reading {file}")
                raise
            
            xsize = band.XSize
            ysize = band.YSize
            for i in range(0, xsize, tile_size_x):
                for j in range(0, ysize, tile_size_y):
                    count += 1
                    tiles['tile_nb'].append(count)
                    tiles['X'].append(coords[0] + i)
                    tiles['Y'].append(coords[3] - j)
                        
                    tiles['origin_file'].append(file.replace('DTM', '{}')) # Replace DTM with {} to be able to format the string later while splitting the tiles
                    tiles['img_pos'].append((i, j))
                    tiles['img_size'].append((tile_size_x, tile_size_y))

        df = pd.DataFrame(tiles)
        df.set_index("tile_nb", inplace=True)
        df.to_csv(self.csv_name)
        return df
    
    @staticmethod
    def get_tile(tiles: pd.DataFrame, coords: Tuple[float, float]) -> pd.Series:
        """
        Find the current tile coresponding to given coordinates
        :param tiles: DataFrame containing each tile with it's coordinates
        :param coords: Tuple coordinates to search for
        :return: Tile Pandas Series
        """
        size = (1000, 500)
        tiles = tiles[(coords[0] > tiles['X']) & (coords[0] < tiles['X'] + size[0])]
        tiles = tiles[(coords[1] < tiles['Y']) & (coords[1] > tiles['Y'] - size[1])]
        if tiles.empty:
            raise Exception("NoMatchingData", "Given coordinates does not exist in tiles data")
        return tiles.iloc[0]

    def split_tile(self, ser: pd.Series) -> None:
        """
        Split specific tile from the big geoTIFF files
        :param ser: Pandas Series containing all the informations
        """
        tile_nb: int = ser.name
        tile_pos: tuple = ser['img_pos']
        tile_size: tuple = ser['img_size']
        origin: str = ser['origin_file']

        for type in ('DTM', 'DSM'):
            input_path = f'{self.data_path.format(type)}{origin.format(type)}/GeoTIFF/{origin.format(type)}.tif'
            output_path = f'{self.tile_path.format(type)}tile_{tile_nb}.tif'
            cmd_str = f'gdal_translate -of GTIFF -srcwin {tile_pos[0]}, {tile_pos[1]}, {tile_size[0]}, {tile_size[1]} {input_path} {output_path}'
            os.system(cmd_str)

    def check_tiff_files(self) -> None:
        """
        Check if folders & files exists before running app, if DTM & DSM have same number of map files
        """
        nb_maps: Dict[str, int] = {}
        for type in ['DTM', 'DSM']:
            # Create tiles folders if they don't exist
            if not os.path.exists(self.tile_path.format(type)):
                os.makedirs(self.tile_path.format(type))
            # Checks if map data exists, if not, raise an Exception
            files = os.listdir(self.data_path.format(type))
            if not os.path.exists(self.data_path.format(type)) or len(files) == 0:
                raise Exception("MapDataError", "Data folder does not exists or is empty")
            # Check if all folders in "data" folder are correclty named (compare nb of files vs nb of files matching regex)
            r = re.compile(r'^DHMVIID[ST]MRAS1m_k[0-9]{2}$')
            if len(files) != len(list(filter(r.match, files))):
                raise Exception("MapDataError", "Map Data folder contains incorrect files")
            nb_maps[type] = len(files)
        if nb_maps['DTM'] != nb_maps['DSM']:
            print("WARNING: You don't have the same amount of DTM and DSM maps, this might cause an issue later")
            


    def clean_tiles(self) -> None:
        """
        Once the program has executed, remove useless files to make place
        """
        for type in ['DTM', 'DSM']:
            path = self.tile_path.format(type)
            # Remove all tiles generated during program execution
            if os.path.exists(path):
                for file in os.listdir(path):
                    os.remove(path + file)