import json
import requests
import matplotlib.pyplot as plt

from typing import Union, Dict
from pyproj import Transformer
from utils.getUserInput import getUserInput

class PolygonRequest:
    """
    This Class will obtain the polygon shape from a API request
    done to the nominatim site. It will also transform the coordinates
    into the Lambert System
    """

    address = ''
    # transformer class is instantiated only once
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:31370", always_xy=True)


    def getJsonInfo(self) -> Union[float, float, Dict]:
        """
        This method will request the coordinates x and y, and
         the polygon of the entered address; convert them into
         Lambert 72 coordinates and then return their values.

        :return: It return the Lambert coordinates XTarget and YTarget
         of the building and the respective polygon
        """

        # We do the request of the address of the building we want to visualize
        # Nollekensstraat 15 as default address located into the split tile 212
        street, houseNumb, postalCode, commune, flagPlots = getUserInput()
        self.address = f'{street} {houseNumb},{postalCode} {commune}'

        # We create the url for the API request
        url = f'https://nominatim.openstreetmap.org/search?format=jsonv2&polygon_geojson=1&q='

        try:
            r = requests.get(url + self.address)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        json_data = json.loads(r.text)

        polygon = list()

        for elem in json_data:
            geojson = elem['geojson']
            if geojson['type'] == 'Polygon':
                polygon = geojson
                break

        # We get the polygon of the building
        if len(polygon) == 0:
            raise Exception('Sorry, polygon or address not found. Please check the address and try again')

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
        if(flagPlots):
            plt.figure(1)
            plt.plot(x, y)
            plt.title('Polygon for ' + street + ' ' + houseNumb)

        return XTarget, YTarget, polygon, flagPlots

    def transformToLambert(self, lon: float, lat: float) -> Union[float, float]:
        """
        This method get a spherical coordinate a transform it into
        Lambert72 coordinates
        :param lon: Longitude to convert
        :param lat: Latitude to convert
        :return: respective Lambert 72 coordinates XTarget, YTarget
        """
        XTarget, YTarget = self.transformer.transform(lon, lat)
        return XTarget, YTarget

