import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple


class Plotter:
    def __init__(self, array_chm: np.ndarray) -> None:
        '''
        expects canopy height model to plot
        
        :param array_chm: chm in ndarray format
        '''
        self.array_chm = array_chm

    def createMesh(self, array_chm: np.ndarray) -> Tuple:
        # we create a grid of same size where elevation data can map on
        col = array_chm.shape[0]
        row = array_chm.shape[1]
        X = np.arange(row)
        Y = np.arange(col)
        X, Y = np.meshgrid(X, Y)
        return tuple((X, Y))

    def createPlot(self) -> None:
        grid = self.createMesh(self.array_chm)
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.plot_surface(grid[0], grid[1], self.array_chm,  rstride=1, cstride=1, cmap='viridis')

        # display it from certain angle
        ax.view_init(30, 135)

        plt.show()
