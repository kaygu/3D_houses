import  numpy as np

def LatLon_To_Lambert72(lat = 51.4711978, lng =4.4677307):

    LongRef = 0.076042943
    bLamb = 6378388 * (1 - (1 / 297))
    aCarre = 6378388**2
    eCarre = (aCarre - bLamb**2) / aCarre
    KLamb = 11565915.812935
    nLamb = 0.7716421928

    eLamb = np.sqrt(eCarre)
    eSur2 = eLamb / 2

    #conversion to radians
    lat = (np.pi / 180) * lat
    lng = (np.pi / 180) * lng

    eSinLatitude = eLamb * np.sin(lat)
    TanZDemi = (np.tan((np.pi / 4) - (lat / 2))) * (((1 + (eSinLatitude)) / (1 - (eSinLatitude)))**(eSur2))
    RLamb = KLamb * TanZDemi**nLamb

    Teta = nLamb * (lng - LongRef)

    x = 0
    y = 0

    x = 150000 + 0.01256 + RLamb * np.sin(Teta - 0.000142043)
    y = 5400000 + 88.4378 - RLamb * np.cos(Teta - 0.000142043)

    return x, y

print('Expected x: 156877.3763564583  y: 240181.21083016414')
print(LatLon_To_Lambert72())
