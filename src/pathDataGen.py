# -*- coding: utf-8 -*-

import numpy as np
# import matplotlib.pyplot as mpplot
# from matplotlib import pyplot
# import pylab
# from mpl_toolkits.mplot3d import Axes3D

RMIN = 200

def plot3(a,b,c,mark="o",col="r"):
    # mimic matlab plot3
    pylab.ion()
    fig = pylab.figure()
    ax = Axes3D(fig)
    ax.invert_zaxis()
    ax.invert_xaxis()
    ax.set_aspect('equal', 'datalim')
    ax.plot(a, b,c,color=col,marker=mark)
    fig.show()
    pyplot.savefig("./trace.png")

def solveEquation(a, b, c):
    x1 = (-b + np.sqrt(np.square(b) - 4*a*c)) / (2 * a)
    x2 = (-b - np.sqrt(np.square(b) - 4*a*c)) / (2 * a)
    return x1, x2


def theataCos(v1, v2):
    return np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))


def pathDataGen(p1, p2, pc, angle):
    v1 = p1 - pc
    v2 = p2 - pc
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    xc, yc, zc = pc
    n = np.cross(v1, v2)
    n1, n2, n3 = n
    angle_d = angle / 1000
    ans = []
    theata_ans = []
    for i in range(1000):
        k1 = -(n3*(x1-xc)-n1*(z1-zc))/(n3*(y1-yc)-n2*(z1-zc))
        c1 = (n3*(np.cos(i*angle_d)*RMIN**2+np.dot(pc, v1))-(z1-zc)*np.dot(n, pc))/(n3*(y1-yc)-n2*(z1-zc))
        k2 = -(n2*(x1-xc)-n1*(y1-yc))/(n2*(z1-zc)-n3*(y1-yc))
        c2 = (n2*(np.cos(i*angle_d)*RMIN**2+np.dot(pc, v1))-(y1-yc)*np.dot(n, pc))/(n2*(z1-zc)-n3*(y1-yc))
        a = 1 + k1**2 + k2**2
        b = -2*(xc - (c1-yc)*k1 - (c2-zc)*k2)
        c = xc**2 + (c1-yc)**2 + (c2-zc)**2 - RMIN**2
        if np.square(b) - 4*a*c < 0:
            pass
        else:
            x_1, x_2 = solveEquation(a, b, c)
            y_1, y_2 = k1*x_1+c1, k1*x_2+c1
            z_1, z_2 = k2*x_1+c2, k2*x_2+c2
            X1 = np.array([x_1, y_1, z_1])
            X2 = np.array([x_2, y_2, z_2])
            theata1_cos = theataCos(X1-pc, v2)
            theata2_cos = theataCos(X2-pc, v2)
            theata_cos = np.cos(angle - i*angle_d)
            if np.abs(theata1_cos-theata_cos) < np.abs(theata2_cos-theata_cos):
                ans.append(X1)
                theata_ans.append([theata1_cos, theata_cos])
            else:
                ans.append(X2)
                theata_ans.append([theata2_cos, theata_cos])
    ans = np.array(ans)
    return ans[:, 0], ans[:, 1], ans[:, 2]
    # plot3(ans[:, 0], ans[:, 1], ans[:, 2])
        # print(angle - i*angle_d)
        # print(i, '\t', theata1_cos, theata2_cos, theata_cos)
