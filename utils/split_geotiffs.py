import os
from osgeo import gdal
import pandas as pd
from typing  import List, Dict, Union, Tuple


def parse_geotiffs(input: str = './data/{}/') -> pd.DataFrame:
    """
    Cycle through every DTM tif files to count how much tiles you have in total
    :arg input_path: Path where your data is stored. './data/{}/' by default.
    :return: dataframe containing all the tiles available
    """
    input_path = input.format('DTM')
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
    df.to_csv('tiles.csv')
    return df

def split_tiles(ser: pd.Series, input: str = './data/{}/', output: str = './data/{}_split/'):
    """
    Split specific tile from the big geoTIFF files
    :arg ser: Pandas Series containing all the informations
    :return: True if success, False if failure
    """
    tile_nb: int = ser.name
    tile_pos:tuple = ser['img_pos']
    tile_size:tuple = ser['img_size']
    origin:str = ser['origin_file']

    for types in ('DTM', 'DSM'):
        input_path = f'{input.format(types)}{origin.format(types)}/GeoTIFF/{origin.format(types)}.tif'
        output_path = f'{output.format(types)}tile_{tile_nb}.tif'
        cmd_str = f'gdal_translate -of GTIFF -srcwin {tile_pos[0]}, {tile_pos[1]}, {tile_size[0]}, {tile_size[1]} {input_path} {output_path}'
        os.system(cmd_str)
    