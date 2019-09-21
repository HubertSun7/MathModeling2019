# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot(p_start, p_end, p_rect, save=''):
    fig = plt.figure(figsize=(9.6, 7.2))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(p_start['coord'][0], p_start['coord'][1], p_start['coord'][2], c='r', label='Start point')
    ax.scatter(p_end['coord'][0], p_end['coord'][1], p_end['coord'][2], c='m', label='Target point')
    coord_rect_v = np.stack([p['coord'] for p in list(filter(lambda n: n['rectVert'], p_rect))], 1)
    coord_rect_h = np.stack([p['coord'] for p in list(filter(lambda n: not n['rectVert'], p_rect))], 1)
    ax.scatter(coord_rect_v[0], coord_rect_v[1], coord_rect_v[2], marker='.', c='b', label='Rectifying points (V)')
    ax.scatter(coord_rect_h[0], coord_rect_h[1], coord_rect_h[2], marker='.', c='y', label='Rectifying points (H)')

    ax.legend(loc='best')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    print('*I* Figure plotted.')

    if not save == '':
        plt.savefig(save, bbox_inches='tight')
        print('*I* Figure saved at %s.' % save)
