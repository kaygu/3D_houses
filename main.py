from utils.split_geotiffs import SplitGeoTiff

# {} = 'DTM' or 'DSM'
INPUT_PATH = './data/{}/'
OUTPUT_PATH = './data/{}_split/'

if __name__ == "__main__":
    # TODO : Check if .tif files are already split to avoid doing it at each run
    # TODO : Build df with every .tif file & coords for faster queries
    thd1 = SplitGeoTiff('DTM', 5, input=INPUT_PATH, output=OUTPUT_PATH)
    thd2 = SplitGeoTiff('DSM', 5, input=INPUT_PATH, output=OUTPUT_PATH)
    thd1.start()
    thd2.start()