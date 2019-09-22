# -*- coding: utf-8 -*-

import time
from dataload import dataset_load
import util
from plot import plot
from question1 import question1
from question2 import question2
from question3 import question3

if __name__ == '__main__':
    args = util.get_args()

    if args.dataset == 1:
        av_param = dict(alpha1=25, alpha2=15, beta1=20, beta2=25,theta=30, delta=0.001)
        p_start, p_end, p_rect = dataset_load('../data/dataset1.xlsx', 'data1')
    else:  # args.dataset == 2
        av_param = dict(alpha1=20, alpha2=10, beta1=15, beta2=20,theta=20, delta=0.001)
        p_start, p_end, p_rect = dataset_load('../data/dataset2.xlsx', 'data2')

    #plot(p_start, p_end, p_rect, save='../out/raw_d%d.png' % args.dataset)

    t_start = time.time()
    if args.question == 1:
        path = question1(p_start, p_end, p_rect, av_param, args.w_astar, args.w1, args.w2)
    elif args.question == 2:
        path = question2(p_start, p_end, p_rect, av_param, args.w_astar, args.w1, args.w2)
    else:  # args.question == 3
        path = question3(p_start, p_end, p_rect, av_param, args.w_astar, args.w1, args.w2, args.w3)
    t_end = time.time()

    plot(p_start, p_end, p_rect, path=path, show=True, save='../out/result_d%d.png' % args.dataset)

    print('*I* Computation takes %.3f sec ... Exit' % (t_end - t_start))
