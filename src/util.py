# -*- coding: utf-8 -*-

import argparse


def get_args():
    parser = argparse.ArgumentParser(description='[MM2019F] UAV Trajectory routing')
    parser.add_argument('--dataset', '-d', metavar='N', type=int, choices=[1, 2], help='Select a dataset 1 or 2')
    parser.add_argument('--question', '-q', metavar='N', type=int, choices=[1, 2, 3], help='Select a question 1, 2 or 3')
    parser.add_argument('--a_star_factor', '-a', metavar='N', type=float, help='set a_star factor')
    args = parser.parse_args()

    return args