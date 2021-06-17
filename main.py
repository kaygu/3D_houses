import pandas as pd
from utils.split_geotiffs import SplitGeoTiff

# {} = 'DTM' or 'DSM'
INPUT_PATH = './data/{}/'
OUTPUT_PATH = './data/{}_split/'

def startup():
    # TODO : Check if .tif files are already split to avoid doing it at each run
    thd1 = SplitGeoTiff('DTM', 3, input=INPUT_PATH, output=OUTPUT_PATH)
    thd2 = SplitGeoTiff('DSM', 3, input=INPUT_PATH, output=OUTPUT_PATH)
    # Start threads
    thd1.start()
    thd2.start()
    # Wait for threads to end
    thd1.join()
    thd2.join()
    # Save tile coordinates to dataframe
    df = pd.DataFrame(thd1.tiles)
    df.set_index('tile', inplace=True)
    df.to_csv('tiles.csv')
    

if __name__ == "__main__":
    startup()