import json
import re
import requests
import matplotlib.pyplot as plt

from typing import Union, Dict
from pyproj import Proj, transform, Transformer


class PolygonRequest:
    """
    This Class will obtain the polygon shape from a API request
    done to the nominatim site. It will also transform the coordinates
    into the Lambert System
    """
    address = ''

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

            print('Please enter the address of the building to plot...\n')
            while True:
                street = input("Street name (Ex. 'Nollekensstraat'): ")
                if re.match(r'^[a-zA-Z-\s]+$', street):
                    break
                print('Please enter a only letters street name')

            while True:
                houseNumb = input("Building number: (Ex. '15'): ")
                if re.match(r'^[0-9]+$', houseNumb):
                    break
                print('Please enter only numbers')

            while True:
                postalCode = input("PostalCode: (Ex. '2910'): ")
                if re.match(r'^[0-9]+$', postalCode):
                    break
                print('Please enter only numbers')

            while True:
                commune = input("Commune: (Ex. 'Essen'): ")
                if re.match(r'^[a-zA-Z\s]+$', commune):
                    break
                print('Please enter only letters')

            # We create the url for the API request

            url = f'https://api.basisregisters.dev-vlaanderen.be/v1/adresmatch?gemeentenaam={commune}&straatnaam={street}&huisnummer={houseNumb}&postCode={postalCode}'

            try:
                r = requests.get(url)
                r.raise_for_status()
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)

            json_data = json.loads(r.text)
            buildingId = json_data['adresMatches'][0]['adresseerbareObjecten'][0]['objectId']
            XTarget, YTarget = json_data['adresMatches'][0]['adresPositie']['point']['coordinates']

            self.address = json_data['adresMatches'][0]['volledigAdres']['geografischeNaam']['spelling']

            url = f'https://api.basisregisters.dev-vlaanderen.be/v1/gebouweenheden/{buildingId}'

            response = requests.get(url)
            json_data = json.loads(response.text)
            objectID = json_data['gebouw']['objectId']

            url = f'https://api.basisregisters.dev-vlaanderen.be/v1/gebouwen/{objectID}'

            response = requests.get(url)
            json_data = json.loads(response.text)

            polygon = json_data['geometriePolygoon']['polygon']['coordinates']
            # We get the polygon of the building
            if len(polygon) == 0:
                raise Exception('Sorry, polygon not found. Please check the address and try again')

            return XTarget, YTarget, polygon
