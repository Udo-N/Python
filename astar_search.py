# This code uses an Astar search to solve a simple number puzzle

import numpy as np
import heapq as hq


# Creating the Priority queue class
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        hq.heapify(self.queue)                      # Turn the queue into a heap

    def push(self, arr, priority):                  # Function to add new array key(for the explored set hash table) to
        hq.heappush(self.queue, (arr, priority))    # the queue/heap along with its priority value, f(n) = g(n) + h(n)

    def pop(self):                                  # This function scans the queue/heap for the array key with the
        if self.queue:                              # lowest f(n) value and pops that array key from the queue
            min_priority = 10000
            min_index = 0
            out = 'Empty'
            for i in range(len(self.queue)):
                value, prior = self.queue[i]
                if prior <= min_priority:
                    min_priority = prior
                    min_index = i
                    out = value
            del self.queue[min_index]
            return out


# Function that takes the 2D array, the location of the open tile('-') in the array, the direction the open tile will be
# moving (1, 2, 3, or 4) and the cost so far, g(n), then outputs a matrix with the new arrangement and the new cost
# If direct is 1, the open tile swaps with the tile above it, 2 swaps with the tile to the left of it, 3 swaps with the
# tile to the right of it, 4 swaps with the tile below it
# If it cannot swap in the direction specified, it returns None
def swap_matrix(arr, open_square, direct, gn):
    new_mat = np.copy(arr)
    row_pos, col_pos = open_square
    if direct == 1 and row_pos != 0:
        new_mat[row_pos, col_pos], new_mat[row_pos-1, col_pos] = arr[row_pos-1, col_pos], arr[row_pos, col_pos]
        gn = gn + 3                                 # cost of swapping above is 3
    elif direct == 2 and col_pos != 0:
        new_mat[row_pos, col_pos], new_mat[row_pos, col_pos-1] = arr[row_pos, col_pos-1], arr[row_pos, col_pos]
        gn = gn + 2                                 # cost of swapping to the left is 2
    elif direct == 3 and col_pos != arr.shape[1] - 1:
        new_mat[row_pos, col_pos], new_mat[row_pos, col_pos+1] = arr[row_pos, col_pos+1], arr[row_pos, col_pos]
        gn = gn + 2                                 # cost of swapping to the right is 2
    elif direct == 4 and row_pos != arr.shape[0] - 1:
        new_mat[row_pos, col_pos], new_mat[row_pos+1, col_pos] = arr[row_pos+1, col_pos], arr[row_pos, col_pos]
        gn = gn + 1                                 # cost of swapping below is 1
    else:
        return None, None
    return new_mat, gn


# obtaining the heuristic cost vaLue, h(n), using the modified manhattan distance formula
def get_h(curr_arr, goal_arr):
    hn = 0
    for row in range(0, curr_arr.shape[0]):
        for col in range(0, curr_arr.shape[1]):
            x = curr_arr[row, col]
            if x != '-':
                rg, cg = np.where(goal_arr == x)
                rg, cg = int(rg), int(cg)
                c = abs(cg - col) * 2
                if (rg - row) > 0:
                    r = (rg - row) * 3
                else:
                    r = abs(rg - row)
                h = c + r
                hn = hn + h
    return hn


# Function to determine the location of the open or unnumbered tile, ('-')
def get_op(mat):
    r_op, c_op = np.where(mat == '-')
    r_op, c_op = int(r_op), int(c_op)
    return r_op, c_op


# Function that compares two arrays and returns True if the arrays are identical
def compArrays(arr1, arr2):
    comparison = arr1 == arr2
    eq = comparison.all()
    return eq


# Function that checks if input 2d array is part of the explored set. Returns True if it is not part of the explored set
def isNotExplored(mat):
    for i in range(1, len(explored_set)):
        if compArrays(explored_set['explored' + str(i)][0], mat):
            return False
    return True


# Setting the initial state of the array
initial = np.array([[2, 8, 3],
                    [6, 7, 4],
                    [1, 5, '-']])

# Setting the goal state of the array
goal = np.array([[1, 2, 3],
                 [8, '-', 4],
                 [7, 6, 5]])

p_queue = PriorityQueue()                                                # Creating the empty priority queue
count = 1
g = 0                                                                    # Initializing cost so far, g(n), as 0
h0 = get_h(initial, goal)                                                # Obtaining estimated cost, h(n)
print(np.array2string(initial).replace('[[', ' [').replace(']]', ']').replace("'", " "), '\n   ', g, '|', h0, '\t \n \t #', count)
current = initial
op = get_op(initial)                                                     # Obtaining initial location of open tile

explored_set = {'explored1': (initial, g, h0)}                           # Initializing explored set hash table with
                                                                         # the initial state

explored_count = 2                                                       # Keeping count of explored states to be later
                                                                         # used in hash table key names

while not compArrays(current, goal):                                     # loops if current state is not equal to goal
    count = count + 1

    # Open tile is moved in all four directions. If the tile can actually be moved in a certain direction, the f(n)
    # value is calculated for the state of the array after it has moved in that direction and added to the explored set
    # along with the array
    mat1, g1 = swap_matrix(current, op, 1, g)
    if mat1 is not None and isNotExplored(mat1):
        h1 = get_h(mat1, goal)
        f1 = g1 + h1
        explored_set['explored' + str(explored_count)] = mat1, g1, h1
        p_queue.push(('explored' + str(explored_count)), f1)
        explored_count = explored_count + 1

    mat2, g2 = swap_matrix(current, op, 2, g)
    if mat2 is not None and isNotExplored(mat2):
        h2 = get_h(mat2, goal)
        f2 = g2 + h2
        explored_set['explored' + str(explored_count)] = mat2, g2, h2
        p_queue.push(('explored' + str(explored_count)), f2)
        explored_count = explored_count + 1

    mat3, g3 = swap_matrix(current, op, 3, g)
    if mat3 is not None and isNotExplored(mat3):
        h3 = get_h(mat3, goal)
        f3 = g3 + h3
        explored_set['explored' + str(explored_count)] = mat3, g3, h3
        p_queue.push(('explored' + str(explored_count)), f3)
        explored_count = explored_count + 1

    mat4, g4 = swap_matrix(current, op, 4, g)
    if mat4 is not None and isNotExplored(mat4):
        h4 = get_h(mat4, goal)
        f4 = g4 + h4
        explored_set['explored' + str(explored_count)] = mat4, g4, h4
        p_queue.push(('explored' + str(explored_count)), f4)
        explored_count = explored_count + 1

    # The highest priority array key is popped to be used to retrieve its respective array from the explored set, and
    # have that array set as the current array along with its g(n) and h(n) values
    current_key = p_queue.pop()
    current, g, h = explored_set[current_key]
    op = get_op(current)                                    # location of open tile in current array is determined

    print(np.array2string(current).replace('[[', ' [').replace(']]', ']').replace("'", " "), '\n   ', g, '|', h, '\t \n \t #', count)

