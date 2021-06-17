import json
from typing import Union, Dict

import requests
import matplotlib.pyplot as plt
from pyproj import Proj, transform


class PolygonRequest():
    polygon_format = '&format=jsonv2&polygon_geojson=1'
    API_url = 'https://nominatim.openstreetmap.org/search?q='

    def getJsonInfo(self, street: str = 'Nollekensstraat', HouseNumb: str = '15') -> Union[float, float, Dict]:
        url = self.API_url + street +  '+' + HouseNumb + self.polygon_format
        print(url)
        response = requests.get(url)

        print(response.text)
        json_data = json.loads(response.text)
        polygon = json_data[1]['geojson']

        # Transforming the spherical coordinates of the house to Lambert 72
        lon, lat = json_data[0]['lon'], json_data[0]['lat']
        XTarget, YTarget = self.transformToLambert(lon, lat)

        # Transforming the spherical coordinates of the polygon to Lambert 72
        for i in range(len(polygon['coordinates'][0])):
            print(i)
            lon, lat = polygon['coordinates'][0][i]
            polygon['coordinates'][0][i] = self.transformToLambert(lon, lat)

        x = [i[0] for i in polygon['coordinates'][0][:]]
        y = [i[1] for i in polygon['coordinates'][0][:]]
        plt.plot(x, y)
        plt.show()

        return XTarget, YTarget, polygon

    def transformToLambert(self, lon: float, lat: float) -> Union[float, float]:
        inProj = Proj(init='epsg:4326')
        outProj = Proj(init='epsg:31370')
        XTarget, YTarget = transform(inProj, outProj, lon, lat)
        return XTarget, YTarget
