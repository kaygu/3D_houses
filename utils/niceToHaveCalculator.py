
from shapely.geometry import Polygon


class NiceToHaveCalculator:
    area = 0
    avg_floors = 0

    def area(self, polygon):
        polygon = Polygon(polygon['coordinates'][0])
        self.area = polygon.area
        print(f'Area: {self.area:.2f} m2')

    def floorsCount(self, array_chm):
        self.avg_floors = array_chm.max()/3.3
        print(f'Floors count (aprox): {int(self.avg_floors)} ')

