import json
from typing import Union, Dict

import requests
import matplotlib.pyplot as plt
from pyproj import Proj, transform, Transformer


class PolygonRequest:
    """
    This Class will obtain the polygon shape from a API request
    done to the nominatim site. It will also transform the coordinates
    into the Lambert System
    """
    polygon_format = '&format=jsonv2&polygon_geojson=1'
    API_url = 'https://nominatim.openstreetmap.org/search?q='

    def getJsonInfo(self, street: str = 'Grens straat', houseNumb: str = '4', postalCode: str = '2910', comune: str = 'Essen') -> Union[float, float, Dict]:
        """
        This method will request the coordinates x and y, and
         the polygon of the entered address; convert them into
         Lambert 72 coordinates and then return their values.

        :param street: The name of the street to look for
        :param houseNumb: The number of the building to look for
        :return: It return the Lambert coordinates XTarget and YTarget
         of the building and the respective polygon
        """

        # We create the url for the API request
        url = self.API_url + street + '+' + houseNumb  + ',' + postalCode  + '+' + comune + self.polygon_format

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        json_data = json.loads(r.text)
        print(json_data)

        polygon = list()

        for elem in json_data:
            geojson = elem['geojson']
            if geojson['type'] == 'Polygon':
                polygon = geojson
                break

        # We get the polygon of the building
        if len(polygon) == 0:
            raise Exception('Sorry, polygon not found. Please check the address and try again')

        # Transforming the spherical coordinates of the house to Lambert 72
        lon, lat = json_data[0]['lon'], json_data[0]['lat']
        XTarget, YTarget = self.transformToLambert(lon, lat)

        # Transforming the spherical coordinates of the polygon to Lambert 72
        for i in range(len(polygon['coordinates'][0])):
            lon, lat = polygon['coordinates'][0][i]
            polygon['coordinates'][0][i] = self.transformToLambert(lon, lat)

        x = [i[0] for i in polygon['coordinates'][0][:]]
        y = [i[1] for i in polygon['coordinates'][0][:]]

        # We plot the polygon
        plt.figure(1)
        plt.plot(x, y)
        plt.title('Polygon for ' + street + ' ' + houseNumb)

        return XTarget, YTarget, polygon

    def transformToLambert(self, lon: float, lat: float) -> Union[float, float]:
        """
        This method get a spherical coordinate a transform it into
        Lambert72 coordinates
        :param lon: Longitude to convert
        :param lat: Latitude to convert
        :return: respective Lambert 72 coordinates XTarget, YTarget
        """
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:31370", always_xy=True)
        XTarget, YTarget = transformer.transform(lon, lat)
        print('Transforming Lat:', lat, ' Lon:', lon, 'to Lambert 72 x:', XTarget,' y:', YTarget)
        return XTarget, YTarget

