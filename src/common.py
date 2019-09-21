import numpy as np
from enum import Enum
import math
import time


class NodeType(Enum):
    Vertical = 1
    Horizontal = 2
    Both = 3
    Start = 4
    Goal = 5


class Label:
    def __init__(self, d, e, f_h, f_v, b, cl, prev, num_prev, num_cur):
        self.d = d                    #与起始点的距离
        self.e = e                    #终点距离预测值
        self.f_h = f_h                  #到达时水平误差
        self.f_v = f_v                  #到达时垂直误差
#       self.b = b                    补充燃料的概率
        self.cl = cl                  #当前位置
        self.prev = prev              #前驱标签
        self.num_prev = num_prev      #前驱结点标签数
        self.num_cur = num_cur        #当前结点标签数


class Loc:
    def __init__(self, point, goal, type = None):
        self.idx = point['index']
        self.pos = point['coord']
        if type is None:
            self.rectVert = NodeType.Vertical if point['rectVert'] else NodeType.Horizontal
        elif type == "goal":
            self.rectVert = NodeType.Goal
        elif type == "start":
            self.rectVert = NodeType.Start
        # TODO: 测试下 sp 应该用什么来测
        # self.sp = np.linalg.norm(self.pos - goal['coord'])
        self.sp = manhattan(self.pos, goal['coord'])
        self.num_label = 0


def cal_distance(point, point2):
    return np.linalg.norm(point.pos - point2.pos)


def manhattan(point, point2):
    return abs(point[0] - point2[0]) +\
           abs(point[1] - point2[1]) +\
           abs(point[2] - point2[2])


def BackTrace(label):
    path = []
    current_label = label
    path.append(current_label.cl)
    while current_label.prev:
        path.append(current_label.prev.cl)
        current_label = current_label.prev
    return path


def back_trace_idx(label):
    path_idx = []
    current_label = label
    path_idx.append(current_label.cl.idx)
    while current_label.prev:
        path_idx.append(current_label.prev.cl.idx)
        current_label = current_label.prev
    return path_idx


def find_neighbours(label, grid, paras):
    links = []
    for p in grid:

        if p in BackTrace(label):
            continue

        err_dis = cal_distance(label.cl, p) * paras['delta']
        if label.cl.rectVert == NodeType.Vertical:
            error_hori = label.f_h + err_dis
            error_vert = err_dis
        elif label.cl.rectVert == NodeType.Horizontal:
            error_hori = err_dis
            error_vert = label.f_v + err_dis
        else:
            error_hori = label.f_h + err_dis
            error_vert = label.f_v + err_dis

        if error_hori < paras['theta'] and error_vert <= paras['theta'] and label.cl != p:
            links.append(p)
    return links


def aStar(start, grid, paras, a_star_factor):

    # For temporary Print
    start_time = time.time()
    min_sp = math.inf
    iter_time = 0

    # Algorithm Begin
    target_reached = False

    openset = set()

    current_label = Label(0, start.sp, 0.0, 0.0, 0.0, start, None, None, 1)
    start.num_label += 1

    # For Debug Use
    # debug_point = 0
    # debug_openset = []

    while target_reached is False:

        # 1. Find all the neighbour locations of current location
        children = find_neighbours(current_label, grid, paras)

        # 2. Decide if add labels to these neighbour locations
        for child in children:

            dis = cal_distance(child, current_label.cl)
            err_dis = dis * paras['delta']
            if current_label.cl.rectVert == NodeType.Vertical:
                error_hori = current_label.f_h + err_dis
                error_vert = err_dis
            elif current_label.cl.rectVert == NodeType.Horizontal:
                error_hori = err_dis
                error_vert = current_label.f_v + err_dis
            else:
                error_hori = current_label.f_h + err_dis
                error_vert = current_label.f_v + err_dis

            if child.rectVert == NodeType.Start:
                continue
            elif child.rectVert == NodeType.Goal:
                openset.add(Label(current_label.d + dis, 0.0, error_hori, error_vert, 0.0, child,
                                  current_label, current_label.cl.num_label,
                                  child.num_label + 1))
                # debug_openset.append(child.idx)
                break
            elif child.rectVert == NodeType.Vertical:
                if error_hori <= paras['alpha2'] and error_vert <= paras['alpha1']:
                    openset.add(Label(current_label.d + dis, child.sp, error_hori, error_vert, 0.0, child,
                                      current_label, current_label.cl.num_label,
                                      child.num_label+1))
                    child.num_label += 1
                    # debug_openset.append(child.idx)
            elif child.rectVert == NodeType.Horizontal:
                if error_hori <= paras['beta2'] and error_vert <= paras['beta1']:
                    openset.add(Label(current_label.d + dis, child.sp, error_hori, error_vert, 0.0, child,
                                      current_label, current_label.cl.num_label,
                                      child.num_label+1))
                    child.num_label += 1
                    # debug_openset.append(child.idx)

        if len(openset) == 0:
            raise ValueError("Can't Find Path")

        # set current_label to the minimal label
        current_label = min(openset, key=lambda o: o.d + a_star_factor * o.e)
        openset.remove(current_label)

        # Temporary Print
        internal_time = time.time()
        elapsed_time = internal_time - start_time
        iter_time += 1
        if current_label.cl.sp < min_sp:
            min_sp = current_label.cl.sp
        if iter_time % 1000 == 0 :
            print("DistanceFromGoal : " + str(min_sp) + "\tIterationTimes : " + str(iter_time) +\
                  "\tElapsedTime : " + str(elapsed_time) + " s" + "\tAstarFac :" +str(a_star_factor))


        ##############################################
        #           For Debug Use
        ##############################################
        # debug_openset.remove(current_label.cl.idx)
        # if current_label.cl.sp < min_sp:
        #     min_sp = current_label.cl.sp
        # print(str(min_sp) + "\t(" + str(current_label.cl.sp) + ")"  + "\t(" + str(current_label.cl.idx) + ")  "\
        #       + str(debug_point))
        # print(BackTraceIdx(current_label))
        # debug_point += 1
        ##############################################



        # whether the child is end
        if current_label.cl.rectVert == NodeType.Goal:
            target_reached = True

    #back Trace
    path = [current_label]
    while current_label.prev:
        path.append(current_label.prev)
        current_label = current_label.prev
    return path[::-1]

