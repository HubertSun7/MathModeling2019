# -*- coding: utf-8 -*-

import common
import numpy as np
import time


def caculate_straight_distance(start, target):
    return np.linalg.norm(start.pos - target.pos)


def question3(p_start, p_end, p_rect, av_param, a_star_factor, w1, w2, w3):
    start_time = time.time()

    grid = []
    start = common.Loc(p_start, p_end, False, 'start')
    for p in p_rect:
        grid.append(common.Loc(p, p_end, p['mayFail']))
    goal = common.Loc(p_end, p_end, False, 'goal')
    grid.append(goal)

    # Get the path
    path = common.aStar(start, grid, av_param, a_star_factor, w1, w2, w3, True, False)

    common.check_path_available(path, av_param)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Output the path
    refPath = []

    f = open("../out/test.csv", "w+")
    print("{:>5}\t{:>18},{:>18},{:>18}\t{:>20}\t{:>20}\t{:>20}\t{:>4}\t{:>5}\t{:>1}" \
          .format("idx", "x", "y", "z", "length", "errorVert", "errorHori", "type", "rate", "mayFail"))

    for i in range(len(path)):
        path_f_max = max(path[i].f_list, key=lambda o : o[0])
        print("{:>5}\t[{:>18},{:>18},{:>18}]\t{:>20}\t{:>20}\t{:>20}\t{:>4}\t{:>.2%}\t{:>1}"\
              .format(str(path[i].cl.idx),
                      str(path[i].cl.pos[0]), str(path[i].cl.pos[1]), str(path[i].cl.pos[2]),
                      str(path[i].d),
                      str(path_f_max[1][1]),
                      str(path_f_max[1][0]),
                      str(1) if path[i].cl.rectVert == common.NodeType.Vertical else str(0),
                      path[i].s_p,
                      str(1) if path[i].cl.isFailPoint else str(0)))

        tmp_type = str(1) if path[i].cl.rectVert == common.NodeType.Vertical else str(0)
        f.write(str(path[i].cl.idx) + "," + str(path_f_max[1][1]) + "," + str(path_f_max[1][0]) + "," +
                tmp_type + "\n")
        refPath.append(str(1) if path[i].cl.rectVert == common.NodeType.Vertical else str(0))

    f.close()
    print("\n\nAstar Factor : " + str(a_star_factor))
    print("Total Nodes: " + str(len(path) - 1))
    print("Total Length: " + str(path[-1].d))
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
