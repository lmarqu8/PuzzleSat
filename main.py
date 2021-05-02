import sys
import pprint
from z3 import *
from timeit import default_timer as timer
import string

db = string.ascii_lowercase + string.ascii_uppercase

def nodes(arr):
    nlist = []
    size = len(arr)
    for x in range(size):
        for y in range(size):
            nlist += [str(x)+str(y)]

    return nlist




def edgesWithStrings(arr):
    size = len(arr)

    vertex = {}

    for x in range(size):
        for y in range(size):
            tempSet = []
            if x > 0: tempSet.append(str(x - 1) + str(y))
            if y > 0: tempSet.append(str(x) + (str(y - 1)))
            if x < size - 1: tempSet.append(str(x + 1) + str(y))
            if y < size - 1: tempSet.append(str(x) + str(y + 1))
            vertex[str(x) + str(y)] = tempSet

    return vertex


def edgesWithTuples(arr):
    size = len(arr)

    vertex = {}

    for x in range(size):
        for y in range(size):
            tempSet = []
            if x > 0: tempSet.append((x - 1, y))
            if y > 0: tempSet.append((x, y - 1))
            if x < size - 1: tempSet.append((x + 1, y))
            if y < size - 1: tempSet.append((x, y + 1))
            vertex[(x, y)] = tempSet

    return vertex


def graph2Sat(arr):
    size = len(arr)
    contains = getUniqueVar(arr)
    numPins = len(contains)
    numSpaces = size ** 2


def variable(arr, nodes):
    variables = {}

    contains = getUniqueVar(arr)

    for a in nodes:
        variables[a] = {}
        for b in contains:
            variables[a][b] = Bool(a + b)

    return variables


def pathFinder(val, arr):
    x = len(arr)
    y = len(arr[0])
    # 1 Get starting point info from val
    startVal, (startX, startY), = val
    s = Solver()


def getUniqueVar(arr):
    toFind = []
    toFindStart = {}
    toFindEnd = {}

    # 1 Find dimensions of arr
    x = len(arr)
    y = len(arr[0])
    # 2 Search for values to link
    for i in range(x):
        for j in range(y):
            if arr[i][j] in db and arr[i][j] not in toFind:
                toFind.append(arr[i][j])
                # toFindStart.append((arr[i][j], (i, j)))
                toFindStart[arr[i][j]] = (i, j)
            elif arr[i][j] in db and arr[i][j] in toFind:
                toFindEnd[arr[i][j]] = (i, j)

    toFind.sort()

    if len(toFind) != len(toFindEnd) or len(toFind) != len(toFindEnd):
        print("Invalid entry, quitting")
        quit(1)

    for i in toFind:
        print(i, toFindStart[i], toFindEnd[i])

    return toFind


if __name__ == '__main__':
    print(sys.version)

    m = 6

    arr1 = [['.' for i in range(m)] for j in range(m)]
    arr1[1][0] = arr1[3][4] = 'a'
    arr1[2][0] = arr1[4][5] = 'b'
    arr1[1][4] = arr1[4][2] = 'c'

    pprint.pprint(variable(arr1, nodes(arr1)))

    tp = edgesWithStrings(arr1)
