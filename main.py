import sys

from z3 import *
import random
from timeit import default_timer as timer
import string

db = string.ascii_lowercase + string.ascii_uppercase


def variable(arr, contains):
    vars = {}
    for i in range(len(arr)):
        vars[i] = {}
        for j in range(len(arr[0])):
            vars[i][j] = {}
            for k in contains:
                coord = "("+str(i)+","+str(j)+")"
                vars[i][j][k] = Bool(coord + k)

    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            for k in contains:
                print(vars[i][j][k], " ", end='')
            print()
        print()
    return vars


def _pathFinder(val, arr):
    x = len(arr)
    y = len(arr[0])
    # 1 Get starting point info from val
    startVal, (startX, startY), = val
    s = Solver()


def pathFinder(arr):
    toFind = []
    toFindStart = []
    toFindEnd = []

    # 1 Find dimensions of arr
    x = len(arr)
    y = len(arr[0])
    # 2 Search for values to link
    for i in range(x):
        for j in range(y):
            if arr[i][j] in db and arr[i][j] not in toFind:
                toFind.append(arr[i][j])
                toFindStart.append((arr[i][j], (i, j)))
            elif arr[i][j] in db and arr[i][j] in toFind:
                toFindEnd.append((arr[i][j], (i, j)))

    print(toFind)
    toFind.sort()

    if len(toFind) != len(toFindEnd) or len(toFind) != len(toFindEnd):
        print("Invalid entry, quitting")
        quit(1)

    # 3 Find paths
    variable(arr, toFind)


if __name__ == '__main__':
    print(sys.version)

    arr1 = [['.' for i in range(5)] for j in range(5)]
    arr1[0][0] = arr1[2][3] = 'a'
    arr1[1][0] = arr1[3][4] = 'b'
    arr1[0][3] = arr1[4][1] = 'c'

    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            print(arr1[i][j], " ", end='')
        print()

    pathFinder(arr1)
