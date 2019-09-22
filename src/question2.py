# -*- coding: utf-8 -*-

import common
import numpy as np
import time
import curves

def caculate_straight_distance(prev, current, next):
    return curves.computeDistance(prev, current, next)


def question2(p_start, p_end, p_rect, av_param, a_star_factor, w1, w2):
    start_time = time.time()

    grid = []
    start = common.Loc(p_start, p_end, False, 'start')
    for p in p_rect:
        grid.append(common.Loc(p, p_end, p['mayFail']))
    goal = common.Loc(p_end, p_end, False, 'goal')
    grid.append(goal)

    grid_dis = [start] +  grid
    # calculate distance matrix
    distance_matrix = {}
    for g_p in grid_dis:
        for g_c in grid_dis:
            for g_n in grid_dis:
                if g_p == goal or g_c == goal:
                    continue
                elif g_n == start:
                    continue
                elif g_c == start:
                    distance_matrix[(None, g_c, g_n)] = np.linalg.norm(g_c.pos - g_n.pos)
                else:
                    distance_matrix[(g_n, g_c, g_n)] = caculate_straight_distance(g_p, g_c, g_n)
    matrix_build_time = time.time()
    print("Matrix Build Time : " + str(matrix_build_time - start_time) + " s")

    # Get the path
    path = common.aStar(start, grid, av_param, a_star_factor, w1, w2, 0, False, distance_matrix, True)

    common.check_path_available(path, av_param)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Output the path
    lengh = 0
    refPath = []

    print("{:>5}\t{:>18},{:>18},{:>18}\t{:>20}\t{:>20}\t{:>20}\t{:>4}\t{:>5}\t{:>1}" \
          .format("idx", "x", "y", "z", "length", "errorVert", "errorHori", "type", "rate", "mayFail"))

    for i in range(len(path)):
        if (i > 0):
            lengh += np.linalg.norm(path[i].cl.pos - path[i - 1].cl.pos)
        path_f_max = max(path[i].f_list, key=lambda o : o[0])
        print("{:>5}\t[{:>18},{:>18},{:>18}]\t{:>20}\t{:>20}\t{:>20}\t{:>4}\t{:>.2%}\t{:>1}"\
              .format(str(path[i].cl.idx),
                      str(path[i].cl.pos[0]), str(path[i].cl.pos[1]), str(path[i].cl.pos[2]),
                      str(lengh),
                      str(path_f_max[1][1]),
                      str(path_f_max[1][0]),
                      str(1) if path[i].cl.rectVert == common.NodeType.Vertical else str(0),
                      path[i].s_p,
                      str(1) if path[i].cl.isFailPoint else str(0)))

        refPath.append(str(1) if path[i].cl.rectVert == common.NodeType.Vertical else str(0))

    print("\n\nAstar Factor : " + str(a_star_factor))
    print("Total Nodes: " + str(len(path) - 1))
    print("Total Length: " + str(lengh))
    print("Success Rate: {:.2f}%".format(path[-1].s_p * 100))
    refPath[0] = "A"
    refPath[-1] = "B"
    print("Ref Path: " + "".join(refPath))


    elapsed_min = 0
    elapsed_hour = 0
    elapsed_sum = elapsed_time

    if elapsed_time > 3600:
        elapsed_hour = int(elapsed_time / 3600.0)
        elapsed_time = elapsed_time % 3600.0

    if elapsed_time > 60:
        elapsed_min = int(elapsed_time / 60.0)
        elapsed_time = elapsed_time % 60.0

    print("\n\nElasped Time : " + str(elapsed_hour) + " h  " + str(elapsed_min) + " m  " + \
          str(elapsed_time) + " s  " + "\t Total Seconds : " + str(elapsed_sum) + " s ")

    return path
