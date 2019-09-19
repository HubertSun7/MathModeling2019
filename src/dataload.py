# -*- coding: utf-8 -*-

import openpyxl
import numpy as np


def dataset_load(path='../data/dataset1.xlsx', sheet='data1'):
    wb = openpyxl.load_workbook(path)
    table = wb[sheet]

    nrows = 0
    start_point = 0
    end_point = 0
    rectify_points = list()
    for row in table.rows:
        nrows += 1
        if nrows == 1 or nrows == 2:
            continue

        line = [col.value for col in row]
        if isinstance(line[4], str):
            point = dict(
                index=line[0],
                coord=np.array([line[1], line[2], line[3]])
            )
            if line[4].startswith('A'):
                start_point = point
            elif line[4].startswith('B'):
                end_point = point
        else:
            rectify_points.append(dict(
                index=line[0],
                coord=np.array([line[1], line[2], line[3]]),
                rectVert=True if line[4] else False,
                mayFail=True if line[5] else False
            ))

    print('*I* Excel table "%s:%s" loaded ... %d rows included.' % (path, sheet, nrows))

    return start_point, end_point, rectify_points
