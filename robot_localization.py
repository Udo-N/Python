import numpy as np
import pandas as pd


# Function to format the print output of the maze for easier viewing
def print2dec(mat):
    ph = np.zeros(mat.shape, dtype=np.ndarray)
    for i in range(0, mat.shape[0]):
        for j in range(0, mat.shape[1]):
            ph[i, j] = np.round(mat[i, j], 2)

    df = pd.DataFrame(data=ph)
    print(df.to_string(header=False, index=False).replace('-1.0', '####'), '\n')


# Function to create an array that stores in each cell the location of obstacles relative to that cell in the maze as a
# [W, N, E, S] list value. For example, if a cell is above it and to the left of it, the list value is [1, 1, 0, 0]
def createLocArr(mat):
    locArr = np.zeros(mat.shape, dtype=np.ndarray)
    for i in range(0, mat.shape[0]):
        for j in range(0, mat.shape[1]):
            loc = [0, 0, 0, 0]
            if mat[i, j] < 0:
                locArr[i, j] = None
            else:
                if (i-1) < 0:
                    loc[1] = 1
                if (i+1) > (mat.shape[0]-1):
                    loc[3] = 1
                if (j-1) < 0:
                    loc[0] = 1
                if (j+1) > (mat.shape[1]-1):
                    loc[2] = 1
                if i != 0 and mat[i-1, j] < 0:
                    loc[1] = 1
                if i != (mat.shape[0]-1) and mat[i+1, j] < 0:
                    loc[3] = 1
                if j != 0 and mat[i, j-1] < 0:
                    loc[0] = 1
                if j != (mat.shape[1]-1) and mat[i, j+1] < 0:
                    loc[2] = 1
                locArr[i, j] = loc
    return locArr


# Function that takes the actual [W, N, E, S] list value and the value sensed by the robot and returns
# P(z=sensed value|s=cell location)
def getPz(loc, sens):
    pz = 1
    for i in range(0, len(loc)):
        # Detecting the obstacle is seen as a positive outcome, the chance of each outcome is multiplied together to
        # get the P(z|s) value. For example if a cell has the value [1, 0, 1, 0] and the sensor detects [1, 1, 0, 0], it
        # would output True Positive * False Positive * False Negative * True Negative respectively
        if loc[i] == 0 and sens[i] == 0:                # The chance of a True Negative is 85%
            pz = pz * 0.85
        elif loc[i] == 1 and sens[i] == 0:              # The chance of a False Negative is 20%
            pz = pz * 0.2
        elif loc[i] == 0 and sens[i] == 1:              # The chance of a False Positive is 15%
            pz = pz * 0.15
        elif loc[i] == 1 and sens[i] == 1:              # The chance of a True Positive is 80%
            pz = pz * 0.8
    return pz


# Function that performs the filtering step on the array, 'mat,' using the evidence, 'sens,' and returns the filtered
# value
def sensing(mat, sens):
    locArr = createLocArr(mat)                          # First, the array with [W, N, E, S] values is created
    pzs = np.zeros(mat.shape, dtype=np.ndarray)         # Another array to store the P(z=sens|s) values is created with
                                                        # the same size as the input array
    mat = mat / 100

    for i in range(0, locArr.shape[0]):
        for j in range(0, locArr.shape[1]):
            if locArr[i, j] is not None:
                pzs[i, j] = getPz(locArr[i, j], sens)   # The pzs array is filled with P(z=sens|s=mat) values

    totalPzs = np.sum(pzs*mat)
    mat = (mat*pzs)/totalPzs                            # Each value in the mat array is multiplied by its respective
                                                        # P(z=sens|s=mat) value and divided by the sum of all
                                                        # P(z=sens|s=mat) values in the pzs array to get P(s=mat|z=sens)
    mat = mat * 100

    for i in range(0, locArr.shape[0]):                 # All obstacles are represented as -1.0 in the array to make the
        for j in range(0, locArr.shape[1]):             # program work
            if mat[i, j] == -0.0:
                mat[i, j] = -1.00
    return mat


# Function that performs the movement step on the array, 'mat,' in the direction, 'direction,' and returns the updated
# array
def moving(mat, direction):
    pss = np.zeros(mat.shape, dtype=np.ndarray)

    # If the movement direction is North, for each cell, it sums the probabilities of the previous cell being each of
    # the cells around it, multiplied by the probability of the robot being in that cell. For example at cell(0,0),
    # there's an 80% chance that the previous cell was the cell below it, cell(1,0), a 10% chance that it was the cell
    # to the right of it, cell(0,1), a 10% chance that it was cell(0,0) itself that just hit the wall and bounced back
    # and 0% chance that it was any other cell. So the P(s2=cell(0,0)|z1=sens) value will be:
    # 0.8 * P(s=cell(1,0)|z=sens) + 0.1 * P(s=cell(0,1)|z=sens) + 0.1 * P(s=cell(0,0)|z=sens)
    # The same principle applies for all direction where there is an 80% chance of the robot moving in the specified
    # direction and a 10% chance of it veering off to each side due to wind
    if direction == 'N':
        for i in range(0, mat.shape[0]):
            for j in range(0, mat.shape[1]):
                if mat[i, j] > 0:

                    if i == 0:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i, j]
                    if i != 0 and mat[i-1, j] < 0:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i, j]
                    if i != mat.shape[0] - 1 and mat[i + 1, j] > 0:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i+1, j]

                    if j == 0 or j == mat.shape[1]-1 or (mat[i, j-1] < 0 and j != 0) or (mat[i, j+1] < 0 and j != mat.shape[1]-1):
                        pss[i, j] = pss[i, j] + 0.1 * mat[i, j]
                    if j != 0 and mat[i, j-1] > 0:
                        pss[i, j] = pss[i, j] + 0.1 * mat[i, j-1]
                    if j != mat.shape[1]-1 and mat[i, j+1] > 0:
                        pss[i, j] = pss[i, j] + 0.1 * mat[i, j+1]

                else:
                    pss[i, j] = -1.0

    elif direction == 'S':
        for i in range(0, mat.shape[0]):
            for j in range(0, mat.shape[1]):
                if mat[i, j] > 0:

                    if i == mat.shape[0]-1:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i, j]
                    if i != mat.shape[0]-1 and mat[i+1, j] < 0:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i, j]
                    if i != 0 and mat[i-1, j] > 0:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i-1, j]

                    if j == 0 or j == mat.shape[1]-1 or (mat[i, j-1] < 0 and j != 0) or (mat[i, j+1] < 0 and j != mat.shape[1]-1):
                        pss[i, j] = pss[i, j] + 0.1 * mat[i, j]
                    if j != 0 and mat[i, j-1] > 0:
                        pss[i, j] = pss[i, j] + 0.1 * mat[i, j-1]
                    if j != mat.shape[1]-1 and mat[i, j+1] > 0:
                        pss[i, j] = pss[i, j] + 0.1 * mat[i, j+1]

                else:
                    pss[i, j] = -1.0

    elif direction == 'W':
        for i in range(0, mat.shape[0]):
            for j in range(0, mat.shape[1]):
                if mat[i, j] > 0:

                    if j == 0:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i, j]
                    if j != 0 and mat[i, j-1] < 0:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i, j]
                    if j != mat.shape[1] - 1 and mat[i, j+1] > 0:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i, j+1]

                    if i == 0 or i == mat.shape[0]-1 or (mat[i-1, j] < 0 and i != 0) or (mat[i+1, j] < 0 and i != mat.shape[0]-1):
                        pss[i, j] = pss[i, j] + 0.1 * mat[i, j]
                    if i != 0 and mat[i-1, j] > 0:
                        pss[i, j] = pss[i, j] + 0.1 * mat[i-1, j]
                    if i != mat.shape[0]-1 and mat[i+1, j] > 0:
                        pss[i, j] = pss[i, j] + 0.1 * mat[i+1, j]

                else:
                    pss[i, j] = -1.0

    elif direction == 'E':
        for i in range(0, mat.shape[0]):
            for j in range(0, mat.shape[1]):
                if mat[i, j] > 0:

                    if j == mat.shape[1]-1:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i, j]
                    if j != mat.shape[1]-1 and mat[i, j+1] < 0:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i, j]
                    if j != 0 and mat[i, j-1] > 0:
                        pss[i, j] = pss[i, j] + 0.8 * mat[i, j-1]

                    if i == 0 or i == mat.shape[0]-1 or (mat[i-1, j] < 0 and i != 0) or (mat[i+1, j] < 0 and i != mat.shape[0]-1):
                        pss[i, j] = pss[i, j] + 0.1 * mat[i, j]
                    if i != 0 and mat[i-1, j] > 0:
                        pss[i, j] = pss[i, j] + 0.1 * mat[i-1, j]
                    if i != mat.shape[0]-1 and mat[i+1, j] > 0:
                        pss[i, j] = pss[i, j] + 0.1 * mat[i+1, j]

                else:
                    pss[i, j] = -1.0
    else:
        print('Error, "', direction, '" is not a specified direction. Must be E, W, N or S')
        return mat

    return pss


# Creating the maze
maze = np.full((6, 7), 2.63)                                        # 2.63% is used because there is an equal chance of
                                                                    # the robot being in any cell
maze[1, 1], maze[1, 4], maze[3, 1], maze[3, 4] = -1, -1, -1, -1     # -1 is used to represent the obstacles in the array
                                                                    # it is not a probability value

# Printing the maze as an array
print('Initial location probabilities')
print2dec(maze)

# Performing each filtering and movement step consecutively as directed
print('Filtering after evidence [0, 0, 0, 0]')
maze = sensing(maze, [0, 0, 0, 0])
print2dec(maze)

print('Prediction after Action N')
maze = moving(maze, 'N')
print2dec(maze)

print('Filtering after evidence [1, 0, 0, 0]')
maze = sensing(maze, [1, 0, 0, 0])
print2dec(maze)

print('Prediction after Action N')
maze = moving(maze, 'N')
print2dec(maze)

print('Filtering after evidence [0, 0, 0, 0]')
maze = sensing(maze, [0, 0, 0, 0])
print2dec(maze)

print('Prediction after Action W')
maze = moving(maze, 'W')
print2dec(maze)

print('Filtering after evidence [0, 1, 0, 1]')
maze = sensing(maze, [0, 1, 0, 1])
print2dec(maze)

print('Prediction after Action W')
maze = moving(maze, 'W')
print2dec(maze)

print('Filtering after evidence [1, 0, 0, 0]')
maze = sensing(maze, [1, 0, 0, 0])
print2dec(maze)
