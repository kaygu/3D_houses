import re
from typing import Tuple


def getUserInput() -> Tuple:
    '''
    Returns the input of the user or the default address
    '''
    print('Please enter a valid address to plot... or just press enter to view Nollekensstraat 15, 2910, Essen')
    while True:
        street = input('Street name: ')
        if re.match(r'^[a-zA-Z\s]+$', street):
            break
        elif street == '':
            street = 'Nollekensstraat'
            break
        print('Please enter a only letters street name')

    while True:
        houseNumb = input('Number: ')
        if re.match(r'^[0-9]+$', houseNumb):
            break
        elif houseNumb == '':
            houseNumb = '15'
            break
        print('Please enter only numbers')

    while True:
        postalCode = input('PostalCode: ')
        if re.match(r'^[0-9]+$', postalCode):
            break
        elif postalCode == '':
            postalCode = '2910'
            break
        print('Please enter only numbers')

    while True:
        comune = input('Comune: ')
        if re.match(r'^[a-zA-Z\s]+$', comune):
            break
        elif comune == '':
            comune = 'Essen'
            break
        print('Please enter only numbers')

    return tuple((street, houseNumb, postalCode, comune))
