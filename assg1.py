from collections import defaultdict
import numpy as np
import copy

rows = 0
cols = 0


def successorFunction(root, frontier, array):
    i, j = root

    if array[i][j] != 1:
        if j == (cols - 1) and i != (rows - 1):
            if array[i + 1][j] != 1:
                frontier.append((i + 1, j))
        elif i == (rows - 1) and j != (cols - 1):
            if array[i][j + 1] != 1:
                frontier.append((i, j + 1))
        elif i != (rows - 1) and j != (cols - 1):
            if array[i][j + 1] != 1:
                frontier.append((i, j + 1))
            if array[i + 1][j] != 1:
                frontier.append((i + 1, j))
            if array[i + 1][j + 1] != 1:
                frontier.append((i + 1, j + 1))

def PathtoCost(path):
    cost = 0;
    for i in range(1, len(path)):
        tempTuple = np.subtract(path[i], path[i - 1])
        comparison = tempTuple == [1, 1]
        value = comparison.all()
        if value:
            cost += 3
        else:
            cost += 2
    return cost

def BFS(root, target, array):
    visited = []
    cost = []
    queue = []

    queue.append([root])

    while queue:
        # Get current Path
        path = queue.pop(0)  # 0 determines FIFO

        # Get first element of path
        vertex = path[-1]

        if vertex == target:
            return path

        if vertex not in visited:
            visited.append(vertex)
            points = []

            # Get next coordinates
            successorFunction(vertex, points, array)

            # Pushing new paths to queue
            for i in points:
                new_path = list(path)
                new_path.append(i)
                queue.append(new_path)

def DFSUtil(start, target, visited, array, path):
    # Mark the current node as visited
    # and print it
    visited.append(start)
    if (start == target):
        return True

    points = []
    successorFunction(start, points, array)
    # Recur for all the vertices
    # adjacent to this vertex
    for i in points:
        if i not in visited:
            if (DFSUtil(i, target, visited, array, path)):
                path.append(i)
                return True

    return False

# recursive DFSUtil()
def DFS(start, target, array):
    global rows
    # Mark all the vertices as not visited
    visited = []
    path = []

    # Call the recursive helper function
    # to print DFS traversal
    DFSUtil(start, target, visited, array, path)

    return path

def IDDFS(root, maxDepth, target, path, array):
    # check if result
    if target == root:
        return True

    # check if 0 depth
    if maxDepth <= 0:
        return False

    # iterate root to its children
    points = []

    successorFunction(root, points, array)
    for i in points:
        if IDDFS(i, maxDepth - 1, target, path, array):
            path.append(i)
            return True;

    return False

def CreateFiles(path, array, name):
    for i in path:
        row, col = i
        array[row][col] = -1

    array.reverse()
    with open(name, 'w') as f:

        for i in array:
            for item in i:
                if item == -1:
                    f.write("* ")
                else:
                    f.write("%s " % item)
            f.write("\n")


def main():
    global rows, cols
    with open("grid.txt", "r+") as f:
        rows, cols = [int(x) for x in next(f).split()]
        starti, startj = [int(x) for x in next(f).split()]
        endi, endj = [int(x) for x in next(f).split()]
        array = [[int(x) for x in line.split()] for line in f]

    f.close()

    array.reverse()
    # cont = createGraph(array,rows,cols)

    t1 = (starti, startj)   #START
    t2 = (endi, endj)   #GOAL

    path1 = []
    path2 = []
    path3 = []

    print("For BFS: ")
    if len(path1) != 0:
        path1 = BFS(t1, t2, array)
        cost1 = PathtoCost(path1)
        print("Path =", path1)
        print("Cost =", cost1)

    print("For IDFS: ")
    if (IDDFS(t1, rows, t2, path2, array)):
        path2.append(t1)
        path2.reverse()
        cost2 = PathtoCost(path2)
        print("Path =", path2)
        print("Cost =", cost2)

    print("For DFS: ")
    path3 = DFS(t1, t2, array)
    if len(path3) != 0:
        path3.reverse()
        cost3 = PathtoCost(path3)
        print("Path =", path3)
        print("Cost =", cost3)

    array1 = copy.deepcopy(array)
    array2 = copy.deepcopy(array)
    array3 = copy.deepcopy(array)

    CreateFiles(path2, array2, "IDDFS.txt")
    CreateFiles(path1, array1, "BFS.txt")
    CreateFiles(path3, array3, "DFS.txt")


if __name__ == "__main__":
    main()
