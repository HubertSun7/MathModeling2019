# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot(p_start, p_end, p_rect, save=''):
    fig = plt.figure()
    fig.set_tight_layout(False)
    ax = Axes3D(fig)

    ax.scatter(p_start['coord'][0], p_start['coord'][1], p_start['coord'][2], c='r', label='Start point')
    ax.scatter(p_end['coord'][0], p_end['coord'][1], p_end['coord'][2], c='b', label='Target point')
    coord_rect = np.stack([p['coord'] for p in p_rect], 1)
    ax.scatter(coord_rect[0], coord_rect[1], coord_rect[2], marker='.', c='gray', label='Rectifying points')

    ax.legend(loc='best')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    print('*I* Figure plotted.')

    if not save == '':
        plt.savefig(save, bbox_inches='tight')
        print('*I* Figure saved at %s.' % save)
