# -*- coding: utf-8 -*-

from dataload import dataset_load
import util
from question1 import question1
from question2 import question2
from question3 import question3

if __name__ == '__main__':
    args = util.get_args()

    if args.dataset == 1:
        q1_av_param = dict(alpha1=25, alpha2=15, beta1=20, beta2=25,theta=30, delta=0.001)
        p_start, p_end, p_rect = dataset_load('../data/dataset1.xlsx', 'data1')
    else:  # args.dataset == 2
        q1_av_param = dict(alpha1=20, alpha2=10, beta1=15, beta2=20,theta=20, delta=0.001)
        p_start, p_end, p_rect = dataset_load('../data/dataset2.xlsx', 'data2')

    if args.question == 1:
        question1(p_start, p_end, p_rect, q1_av_param)
    elif args.question == 2:
        question2(p_start, p_end, p_rect)
    else:  # args.question == 3
        fail_rate = 0.8
        err_threshold = 5
        question3(p_start, p_end, p_rect, fail_rate, err_threshold)

    print('*I* Computation complete ... Exit')
