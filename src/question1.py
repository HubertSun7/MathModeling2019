# -*- coding: utf-8 -*-

import common
import numpy as np
import time


def question1(p_start, p_end, p_rect, av_param, a_star_factor):

    start_time = time.time()

    #Convert all the points to instances of Node
    # grid = []
    # start = common.Node(p_start, 'start')
    # for p in p_rect:
    #     grid.append(common.Node(p))
    # goal = common.Node(p_end, 'goal')
    # grid.append(goal)
    grid = []
    start = common.Loc(p_start, p_end, 'start')
    for p in p_rect:
        grid.append(common.Loc(p, p_end))
    goal = common.Loc(p_end, p_end, 'goal')
    grid.append(goal)


    #Get the path
    path = common.aStar(start, grid, av_param, a_star_factor)

    end_time = time.time()
    elapsed_time = end_time - start_time

    #Output the path
    lengh = 0
    refPath = []

    print("{:>5}\t{:>18},{:>18},{:>18}\t{:>20}\t{:>20}\t{:>20}\t{:>1}"\
          .format("idx","x", "y", "z", "length", "errorVert", "errorHori", "type"))

    for i in range(len(path)):
        if (i > 0):
            lengh += np.linalg.norm(path[i].cl.pos - path[i-1].cl.pos)
        print("{:>5}\t[{:>18},{:>18},{:>18}]\t{:>20}\t{:>20}\t{:>20}\t{:>4}"\
              .format(str(path[i].cl.idx),
                      str(path[i].cl.pos[0]), str(path[i].cl.pos[1]), str(path[i].cl.pos[2]),
                      str(lengh),
                      str(path[i].f_v),
                      str(path[i].f_h),
                      str(1) if path[i].cl.rectVert == common.NodeType.Vertical else str(0)))

        refPath.append( str(1) if path[i].cl.rectVert == common.NodeType.Vertical else str(0))

    print("\n\nAstar Factor : " + str(a_star_factor))
    print("Total Nodes: " + str(len(path)-1))
    print("Total Length: " + str(lengh))
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

    print("Elasped Time : " + str(elapsed_hour) + " h  " + str(elapsed_min) + " m  " + \
          str(elapsed_time) + " s  " + "\t Total Seconds : "  + str(elapsed_sum) + " s ")




