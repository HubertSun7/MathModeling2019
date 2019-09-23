# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathDataGen import *
from curves import *


def linePathGen(p0, p1):
    zline = np.arange(p0[2], p1[2], (p1[2] - p0[2]) / 1000.0)
    yline = np.arange(p0[1], p1[1], (p1[1] - p0[1]) / 1000.0)
    xline = np.arange(p0[0], p1[0], (p1[0] - p0[0]) / 1000.0)
    return xline, yline, zline


def plot(p_start, p_end, p_rect, question, path=None, show=False, save=''):
    fig = plt.figure(figsize=(9.6, 7.2))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(p_start['coord'][0], p_start['coord'][1], p_start['coord'][2], c='r', label='Start point')
    ax.scatter(p_end['coord'][0], p_end['coord'][1], p_end['coord'][2], c='m', label='Target point')
    coord_rect_v = np.stack([p['coord'] for p in list(filter(lambda n: n['rectVert'], p_rect))], 1)
    coord_rect_h = np.stack([p['coord'] for p in list(filter(lambda n: not n['rectVert'], p_rect))], 1)
    ax.scatter(coord_rect_v[0], coord_rect_v[1], coord_rect_v[2], marker='.', c='b', label='Rectifying points (V)')
    ax.scatter(coord_rect_h[0], coord_rect_h[1], coord_rect_h[2], marker='.', c='y', label='Rectifying points (H)')

    if path is not None:
        if question != 2:
            cnt_path = len(path)
            for i in range(cnt_path - 1):
                p0 = path[i].cl.pos
                p1 = path[i + 1].cl.pos
                xline, yline, zline = linePathGen(p0, p1)
                ax.plot3D(xline[0:1000], yline[0:1000], zline[0:1000], 'black')
        else:
            cnt_path = len(path)
            for i in range(cnt_path-1):
                if i == 0:
                    p0 = path[i].cl.pos
                    p1 = path[i+1].cl.pos
                    xline, yline, zline = linePathGen(p0, p1)
                    ax.plot3D(xline[0:1000], yline[0:1000], zline[0:1000], 'black')
                else:
                    p0 = path[i-1].cl.pos
                    p1 = path[i].cl.pos
                    p2 = path[i+1].cl.pos
                    distance, pos_circle, pos_tang, angle = computeDistance(p0, p1, p2)
                    if angle == 0:
                        xline, yline, zline = linePathGen(p1, p2)
                        ax.plot3D(xline, yline, zline, 'black')
                    else:
                        xline, yline, zline = pathDataGen(p1, pos_tang, pos_circle, angle)
                        ax.plot3D(xline, yline, zline, 'r')
                        xline, yline, zline = linePathGen(pos_tang, p2)
                        ax.plot3D(xline[0:1000], yline[0:1000], zline[0:1000], 'black')

    ax.legend(loc='best')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    if show:
        plt.show()
        print('*I* Figure plotted ... You may need to close the figure window to continue')

    if not save == '':
        plt.savefig(save, bbox_inches='tight')
        print('*I* Figure saved at %s.' % save)
