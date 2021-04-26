import sys

from z3 import *
import random
from timeit import default_timer as timer
import string

db = string.ascii_lowercase + string.ascii_uppercase


def _pathFinder(val, arr):
    x = len(arr)
    y = len(arr[0])
    # 1 Get starting point info from val
    startVal, startX, startY, = val
    s = Solver()


def pathFinder(arr):
    toFind = []
    toFindWithStart = []

    # 1 Find dimensions of arr
    x = len(arr)
    y = len(arr[0])
    # 2 Search for values to link
    for i in range(x):
        for j in range(y):
            if arr[i][j] in db and arr[i][j] not in toFind:
                toFind.append(arr[i][j])
                toFindWithStart.append((arr[i][j], i, j))

    print(toFind)
    print(toFindWithStart)
    # 3 Find paths
    for i in toFindWithStart:
        _pathFinder(i, arr)


if __name__ == '__main__':
    print(sys.version)

    arr1 = [['.' for i in range(3)] for j in range(3)]
    arr1[0][0] = 'A'
    arr1[2][2] = 'A'

    pathFinder(arr1)
