import numpy as np
import matplotlib.pyplot as plt


def _3dPlot(array):
    '''
    
    '''
    col = array.shape[0]
    row = array.shape[1]

    # we create a grid where elevation data can map on
    X = np.arange(row)
    Y = np.arange(col)
    X, Y = np.meshgrid(X, Y)


    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(X, Y, array, cmap='viridis', edgecolor='none')
    # ax.plot_wireframe(X, Y, array_dtm, color='black')
    ax.view_init(30,135)
    # ax.set_zlim(6,13)
    # ax.invert_zaxis()
    plt.show()

