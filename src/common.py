import numpy as np
from enum import Enum
import math
import time
import heapq

# 矫正点概率
p_rect_success = 0.8
threshold = 5

class NodeType(Enum):
    Vertical = 1
    Horizontal = 2
    Both = 3
    Start = 4
    Goal = 5


class Label:
    def __init__(self, d, n, e, f, cl, prev, num_prev, num_cur):
        self.d = d                    #与起始点的距离
        self.n = n                    #与起始点的点数距离
        self.e = e                    #终点距离预测值
        self.f_list = []              #到达时的误差list [(概率 : 到达燃料 (f_h, f_v))]
                                      # f_h : 到达时的水平误差
                                      # f_v : 到达时的垂直误差
        self.cl = cl                  #当前位置
        self.prev = prev              #前驱标签
        self.num_prev = num_prev      #前驱结点标签数
        self.num_cur = num_cur        #当前结点标签数

        for f_i in f:
            # f_i 的格式： ( 概率, (f_h, f_v))
            self.f_list.append(f_i)

        self.s_p = sum([f_i[0] for f_i in self.f_list])  # 成功到达当前结点的概率

        self.cost = None                #Label 的 cost

    def set_cost(self, cost):
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

class Loc:
    def __init__(self, point, goal, isFailPoint, type=None):
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
        self.isFailPoint =  isFailPoint       #当前结点是否会发生失败的情况


def cal_distance(point, point2, distance_matrix, prev_point, useCurve):
    return_value = None
    if (useCurve):
        return_value = distance_matrix[(prev_point, point, point2)]
    else:
        return_value = distance_matrix[(point, point2)]
    return return_value

def manhattan(point, point2):
    return abs(point[0] - point2[0]) +\
           abs(point[1] - point2[1]) +\
           abs(point[2] - point2[2])


def back_trace(label):
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


def error_in_next_node(f_h, f_v, current_loc, next_loc, delta, p, considerP, distance_matrix, prev_loc, useCurve):
    # 格式：[概率 : 到达误差 (error_hori, error_vert)]
    err_dict = []

    if considerP and current_loc.isFailPoint:
        p_success = p_rect_success
    else:
        p_success = 1.0

    err_dis = cal_distance(current_loc, next_loc, distance_matrix, prev_loc ,useCurve) * delta
    if current_loc.rectVert == NodeType.Vertical:
        error_hori = f_h + err_dis
        error_vert = err_dis
        err_dict.append( (p*p_success, (error_hori, error_vert)) )
        if considerP and current_loc.isFailPoint:
            error_hori_r = f_h + err_dis
            error_vert_r = min(f_v, threshold) + err_dis
            err_dict.append( (p*(1-p_success), (error_hori_r, error_vert_r)) )
    elif current_loc.rectVert == NodeType.Horizontal:
        error_hori = err_dis
        error_vert = f_v + err_dis
        err_dict.append( (p*p_success, (error_hori, error_vert)) )
        if considerP and current_loc.isFailPoint:
            error_hori_r = min(f_h, threshold) + err_dis
            error_vert_r = f_v + err_dis
            err_dict.append( (p*(1-p_success), (error_hori_r, error_vert_r)) )
    else:
        error_hori = f_h + err_dis
        error_vert = f_v + err_dis
        err_dict.append( (p, (error_hori, error_vert)) )

    return err_dict


def find_neighbours(label, grid, paras, considerP, distance_matrix, useCurve):
    links = []
    for p in grid:

        if p in back_trace(label):
            continue

        # add to link if one of the (f_h, f_v) pair can satisfy the requirement
        added = False
        for (p_f, f) in label.f_list:
            f_h = f[0]
            f_v = f[1]
            prev_loc = None if label.cl.rectVert == NodeType.Start else label.prev.cl
            error_list = error_in_next_node(f_h, f_v, label.cl, p, paras['delta'], p_f,
                                            considerP, distance_matrix, prev_loc, useCurve)

            for (p_el, err_el) in error_list:
                error_hori = err_el[0]
                error_vert = err_el[1]
                if error_hori <= paras['theta'] and error_vert <= paras['theta'] and label.cl != p:
                    links.append(p)
                    added = True
                    break

            if added is True:
                break

    return links


def aStar(start, grid, paras, a_star_factor, w1, w2, w3, considerP, distance_matrix, useCurve):

    # For temporary Print
    start_time = time.time()
    min_sp = math.inf
    iter_time = 0

    # Algorithm Begin
    target_reached = False

    openset = []

    current_label = Label(0, 0, start.sp, [(1.0, (0.0, 0.0))], start, None, None, 1)
    cost = (w1 * current_label.d + w2 * current_label.n + w3 / current_label.s_p) + a_star_factor * current_label.e
    current_label.set_cost(cost)
    start.num_label += 1


    # For Debug Use
    # debug_point = 0
    debug_openset = []

    while target_reached is False:

        # 1. Find all the neighbour locations of current location
        children = find_neighbours(current_label, grid, paras, considerP, distance_matrix, useCurve)

        # 2. Decide if add labels to these neighbour locations
        for child in children:

            prev_loc = None if current_label.cl.rectVert == NodeType.Start else current_label.prev.cl
            dis = cal_distance(child, current_label.cl, distance_matrix, prev_loc, useCurve)

            prev_loc = None if current_label.cl.rectVert == NodeType.Start else current_label.prev.cl
            child_f_cell = []
            for (p, f) in current_label.f_list:
                f_h = f[0]
                f_v = f[1]
                error_list = error_in_next_node(f_h, f_v, current_label.cl,
                                                child, paras['delta'], p, considerP, distance_matrix, prev_loc, useCurve)
                for (p_el, err_el) in error_list:
                    error_hori = err_el[0]
                    error_vert = err_el[1]
                    if (child.rectVert == NodeType.Goal and
                            error_hori <= paras['theta'] and error_vert <= paras['theta'])\
                        or (child.rectVert == NodeType.Vertical and
                            error_hori <= paras['alpha2'] and error_vert <= paras['alpha1'])\
                        or (child.rectVert == NodeType.Horizontal and
                            error_hori <= paras['beta2'] and error_vert <= paras['beta1']):
                        child_f_cell.append((p_el, (error_hori, error_vert)))

            if child.rectVert == NodeType.Start:
                continue
            elif child.rectVert == NodeType.Goal:
                c_L = Label(current_label.d + dis, current_label.n + 1,
                            0.0, child_f_cell, child,
                            current_label, current_label.cl.num_label,
                            child.num_label + 1)
                cost = (w1 * c_L.d + w2 * c_L.n + w3 / c_L.s_p) + a_star_factor * c_L.e
                c_L.set_cost(cost)
                heapq.heappush(openset, c_L)
                child.num_label += 1
                debug_openset.append(child.idx)
                break
            elif child.rectVert == NodeType.Vertical:
                if len(child_f_cell) != 0:
                    c_L = Label(current_label.d + dis, current_label.n + 1,
                                child.sp, child_f_cell, child,
                                current_label, current_label.cl.num_label,
                                child.num_label + 1)
                    child.num_label += 1
                    cost = (w1 * c_L.d + w2 * c_L.n + w3 / c_L.s_p) + a_star_factor * c_L.e
                    c_L.set_cost(cost)
                    heapq.heappush(openset, c_L)
                    debug_openset.append(child.idx)
            elif child.rectVert == NodeType.Horizontal:
                if len(child_f_cell) != 0:
                    c_L = Label(current_label.d + dis, current_label.n + 1,
                                      child.sp, child_f_cell, child,
                                      current_label, current_label.cl.num_label,
                                      child.num_label+1)
                    cost = (w1*c_L.d + w2*c_L.n + w3/c_L.s_p) + a_star_factor * c_L.e
                    c_L.set_cost(cost)
                    heapq.heappush(openset, c_L)
                    child.num_label += 1
                    debug_openset.append(child.idx)

        if len(openset) == 0:
            raise ValueError("Can't Find Path")

        # set current_label to the minimal label
        # Cost Function = G(n) + H(n)
        # G(n) = (w1 * distance + w2 + w3 / possibility)
        # H(n) = a_start_factor * estimated_cost
        current_label = heapq.heappop(openset)

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
        debug_openset.remove(current_label.cl.idx)
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



def check_path_available(path, paras):
    for i in range(len(path)):
        # 1、判断这条路的完整性：当前结点的后继结点的前驱结点为当前结点
        if (i < len(path)-1):
            if (path[i+1].prev == path[i]) is not True:
                raise ValueError("Error path : not complete")

        # 2、检查当前结点所有 f_h, f_v 是否满足校准要求
        if i > 0:
            for (_, f) in path[i].f_list:
                f_h = f[0]
                f_v = f[1]
                isSatisfied = ((path[i].cl.rectVert == NodeType.Goal and
                    f_h <= paras['theta'] and f_v <= paras['theta'])
                    or (path[i].cl.rectVert == NodeType.Vertical and
                        f_h <= paras['alpha2'] and f_v <= paras['alpha1'])
                    or (path[i].cl.rectVert == NodeType.Horizontal and
                        f_h <= paras['beta2'] and f_v <= paras['beta1']))
                if not isSatisfied:
                    raise ValueError("Error path : wrong flying error in current node :" + str(path[i].cl.idx))

