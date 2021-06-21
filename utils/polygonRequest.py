import json
from typing import Union, Dict

import requests
import matplotlib.pyplot as plt
from pyproj import Proj, transform, Transformer


class PolygonRequest:
    polygon_format = '&format=jsonv2&polygon_geojson=1'
    API_url = 'https://nominatim.openstreetmap.org/search?q='

    def getJsonInfo(self, street: str = 'Nollekensstraat', houseNumb: str = '15') -> Union[float, float, Dict]:
        street.replace(' ', '+')
        url = self.API_url + street + '+' + houseNumb + self.polygon_format
        response = requests.get(url)

        json_data = json.loads(response.text)
        polygon = json_data[0]['geojson']

        # Transforming the spherical coordinates of the house to Lambert 72
        lon, lat = json_data[0]['lon'], json_data[0]['lat']
        XTarget, YTarget = self.transformToLambert(lon, lat)

        # Transforming the spherical coordinates of the polygon to Lambert 72
        for i in range(len(polygon['coordinates'][0])):
            lon, lat = polygon['coordinates'][0][i]
            polygon['coordinates'][0][i] = self.transformToLambert(lon, lat)

        x = [i[0] for i in polygon['coordinates'][0][:]]
        y = [i[1] for i in polygon['coordinates'][0][:]]
        plt.plot(x, y)
        plt.title('Polygon for ' + street + ' ' + houseNumb)
        plt.show()

        return XTarget, YTarget, polygon

    def transformToLambert(self, lon: float, lat: float) -> Union[float, float]:
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:31370", always_xy=True)
        XTarget, YTarget = transformer.transform(lon, lat)
        print('Transforming Lat:', lat, ' Lon:', lon, 'to Lambert 72 x:', XTarget,' y:', YTarget)
        return XTarget, YTarget

