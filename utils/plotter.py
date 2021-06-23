from matplotlib import pylab as pl
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple


class Plotter:
    def __init__(self, array_chm: np.ndarray) -> None:
        '''
        expects and initializes with canopy height model to plot. 
        then it plots in 3d
        
        :param array_chm: chm in ndarray format
        '''
        self.pad_width = 5
        self.array_chm = self.addPadding(array_chm)

    def addPadding(self, array_chm: np.ndarray) -> np.ndarray:
        # add padding around the shape to reduce deformations
        array_chm = np.pad(array_chm, pad_width=self.pad_width, mode='constant', constant_values=0)
        return array_chm

    def createMesh(self, array_chm: np.ndarray) -> Tuple:
        # create a grid of same size where elevation data can map on
        col = array_chm.shape[0]
        row = array_chm.shape[1]
        X = np.arange(row)
        Y = np.arange(col)
        X, Y = np.meshgrid(X, Y)
        return tuple((X, Y))

    def createPlot(self, adressName: str) -> None:
        # creates the plot based on the mesh created and shows that

        grid = self.createMesh(self.array_chm)
        fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw=dict(projection='3d'))
        surf = ax.plot_surface(grid[0], grid[1], self.array_chm, rstride=1, cstride=1, linewidth=0, antialiased=False, lw=0, cmap='viridis')
        fig.colorbar(surf, ax=ax)
        ax.set(title=adressName)
        
        plt.show()
