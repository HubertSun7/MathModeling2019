# -*- coding: utf-8 -*-

import argparse


def get_args():
    parser = argparse.ArgumentParser(description='[MM2019F] UAV Trajectory routing')
    parser.add_argument('--dataset', '-d', metavar='N', type=int, choices=[1, 2], help='Select a dataset 1 or 2')
    parser.add_argument('--question', '-q', metavar='N', type=int, choices=[1, 2, 3], help='Select a question 1, 2 or 3')
    parser.add_argument('--w_astar', '-a', metavar='N', type=float, help='Set the factor of estimated cost ')
    parser.add_argument('--w1', '-w1', metavar='N', type=float, help='Set the weight of distance from A')
    parser.add_argument('--w2', '-w2', metavar='N', type=float, help='Set the weight of rectifying times')
    parser.add_argument('--w3', '-w3', metavar='N', type=float, help='Set the weight of success probability')
    args = parser.parse_args()

    return args
