"""
    File:               Mazes.py
    Associated Files:
    Packages Needed:    random, deepcopy(copy)
    Date Created:       8/1/2020
    Author:             John Lukowski
    Date Modified:      8/9/2020 by John Lukowski (added comments)
    License:            CC-BY-SA-4.0

    Purpose:            Simple teaching example for creating/solving mazes.
                        after going through these have the students research and implement their own solver or gen
"""

from copy import deepcopy
import random

"""
    Function:   saveMaze
    Params :    (2d char list) maze
                (string) fileName
    Returns:    none
    Purpose:    print out the maze to the given file, erase or create it first.
"""
def saveMaze(maze, fileName):
    with open(fileName, 'w') as file:
        for row in maze:
            file.write(''.join(row)+'\n')

"""
    Function:   loadMaze
    Params :    (string) fileName
    Returns:    (2d char list)
    Purpose:    load the maze from the given file, no error checking currently
    ### WARNING: MAY THROW ERRORS IF INVALID FILE ###
"""
def loadMaze(fileName):
    with open(fileName) as file:
        return [[char for char in line.strip()] for line in file]

"""
    Function:   blankMaze
    Params :    (int) size
    Returns:    (2d char list)
    Purpose:    generate a maze full of walls, only odd sizes allowed, so add 1 to an even size
"""
def blankMaze(size):
    maze = []
    if size % 2 == 0:
        size += 1
    for row in range(size):
        currRow = []
        for col in range(size):
            currRow.append('#' if row%2==0 or col%2==0 else ' ')
        maze.append(currRow)
    return maze

"""
    Function:   printMaze
    Params :    (2d char list)
    Returns:    none
    Purpose:    pretty print given 2d maze
"""
def printMaze(maze):
    for row in maze:
        for col in row:
            print(col, end=' ')
        print()
    print()

"""
    Function:   printMaze
    Params :    (int tuple) cell
                (2d char list) mazeVisited
    Returns:    (1d bool list)
    Purpose:    bool whether each direction is in the maze and untouched/empty
"""
def getNeighbors(cell, mazeVisited):
    neighbors = [False,False,False,False]
    cellX = cell[1]
    cellY = cell[0]
    # Check bounds, then check if visited
    if cellX > 2:
        neighbors[0] = mazeVisited[cellY][cellX-2] == ' '
    if cellY > 2:
        neighbors[1] = mazeVisited[cellY-2][cellX] == ' '
    if cellX < len(mazeVisited)-2:
        neighbors[2] = mazeVisited[cellY][cellX+2] == ' '
    if cellY < len(mazeVisited)-2:
        neighbors[3] = mazeVisited[cellY+2][cellX] == ' '
    return neighbors

"""
    Function:   dfMazeGen
    Params :    (2d char list) maze
                (2d char list) mazeVisited
                (1d int tuple list) cells
    Returns:    (True) for complete
    Purpose:    Should really make a helper function for calling this so they only have to give it maze
                removes walls in-place in maze until a perfect maze is made
"""
def dfMazeGen(maze,mazeVisited,cells):
    # Backtracked to start, done creation
    if len(cells) <= 0:
        return True
    cell = cells[-1]
    # Visit current cell
    mazeVisited[cell[0]][cell[1]] = '*'
    # Check each direction to see if it has been visited yet and its in the maze
    neighbors = getNeighbors(cell, mazeVisited)
    if any(neighbors):
        # weighted direction picking to make different maze patterns, could just do dir = random.randint(0,3)
        # Makes sure the direction is valid, easier ways to do this but usually more complicated
        dir = random.randint(0,100)
        if dir < 10:    dir = 0
        elif dir < 50:  dir = 1
        elif dir < 60:  dir = 2
        else:           dir = 3
        while not neighbors[dir]:
            dir = random.randint(0, 100)
            if dir < 10:    dir = 0
            elif dir < 50:  dir = 1
            elif dir < 60:  dir = 2
            else:   dir = 3
        # remove the wall in the chosen direction
        if dir == 0:
            cell = (cell[0],cell[1]-2)
            maze[cell[0]][cell[1]+1] = ' '
        elif dir == 1:
            cell = (cell[0]-2, cell[1])
            maze[cell[0]+1][cell[1]] = ' '
        elif dir == 2:
            cell = (cell[0],cell[1]+2)
            maze[cell[0]][cell[1] - 1] = ' '
        else:
            cell = (cell[0]+2, cell[1])
            maze[cell[0] - 1][cell[1]] = ' '
        # Move to the new cell
        cells.append(cell)
        return dfMazeGen(maze,mazeVisited,cells)
    # No valid directions to move, backtrack
    cells.pop()
    return dfMazeGen(maze,mazeVisited,cells)

"""
    Function:   dfMazeSolver
    Params :    (2d char list) maze
                (2d char list) mazeVisited
                (1d int tuple list) cells
                (int tuple) finish
    Returns:    (False) for unsolvable or (1d int tuple list) path to finish
    Purpose:    Should really make a helper function for calling this so they only have to give it maze,start,finish
                Searches from start to finish, hugs left wall, returns first path found
"""
def dfMazeSolver(maze, visitedMaze, cells, finish):
    # Backtracked to start, no valid path found
    if len(cells) <= 0:
        return False
    cell = cells[-1]
    # Visit current cell
    visitedMaze[cell[0]][cell[1]] = '*'
    if cell == finish:
        return cells
    # Check each direction to see if it has been visited yet and its in the maze
    neighbors = getNeighbors(cell, visitedMaze)
    # For each valid direction, if there is no wall, move there
    if neighbors[0] and maze[cell[0]][cell[1]-1] != '#':
        cells.append((cell[0],cell[1]-2))
        return dfMazeSolver(maze, visitedMaze, cells, finish)
    if neighbors[1] and maze[cell[0]-1][cell[1]] != '#':
        cells.append((cell[0]-2, cell[1]))
        return dfMazeSolver(maze, visitedMaze, cells, finish)
    if neighbors[2] and maze[cell[0]][cell[1]+1] != '#':
        cells.append((cell[0],cell[1]+2))
        return dfMazeSolver(maze, visitedMaze, cells, finish)
    if neighbors[3] and maze[cell[0]+1][cell[1]] != '#':
        cells.append((cell[0]+2, cell[1]))
        return dfMazeSolver(maze, visitedMaze, cells, finish)
    # There were no valid directions to move in, backtrack
    cells.pop()
    return dfMazeSolver(maze, visitedMaze, cells, finish)

"""
    Function:   aStarSolver
    Params :    (2d char list) maze
                (2d char list) mazeVisited
                (1d int tuple list) cells
                (int tuple) finish
    Returns:    (False) for unsolvable or (1d int tuple list) path to finish
    Purpose:    Should really make a helper function for calling this so they only have to give it maze,start,finish
                Searches from start to finish, checks all paths
                Could utilize parallel computing to check all paths at once, would end when the first one is found
"""
def aStarSolver(maze, visitedMaze, cells, finish):
    # Visit current cell
    cell = cells[-1]
    visitedMaze[cell[0]][cell[1]] = '*'
    if cell == finish:
        return cells
    # Check each direction to see if it has been visited yet and its in the maze
    neighbors = getNeighbors(cell, visitedMaze)
    paths = [None]*4
    # For each traversable path that doesnt overlap (could cause issues if not parallel computing), find its path to the finish
    if neighbors[0] and maze[cell[0]][cell[1]-1] != '#':
        temp = deepcopy(cells)
        temp.append((cell[0],cell[1]-2))
        paths[0] = aStarSolver(maze, visitedMaze, temp, finish)
    if neighbors[1] and maze[cell[0]-1][cell[1]] != '#':
        temp = deepcopy(cells)
        temp.append((cell[0]-2, cell[1]))
        paths[1] = aStarSolver(maze, visitedMaze, temp, finish)
    if neighbors[2] and maze[cell[0]][cell[1]+1] != '#':
        temp = deepcopy(cells)
        temp.append((cell[0],cell[1]+2))
        paths[2] = aStarSolver(maze, visitedMaze, temp, finish)
    if neighbors[3] and maze[cell[0]+1][cell[1]] != '#':
        temp = deepcopy(cells)
        temp.append((cell[0]+2, cell[1]))
        paths[3] = aStarSolver(maze, visitedMaze, temp, finish)
    # If no traversable paths to the finish, return unsolvable from this cell
    if not any(paths):
        return False
    # Otherwise, return the shortest path
    shortest = [None]*len(maze)**2
    for path in paths:
        if path and len(path)<len(shortest):
            shortest = path
    return shortest

mazeSize = 7
maze = blankMaze(mazeSize)
dfMazeGen(maze, deepcopy(maze), [(1,1)])
printMaze(maze)

#path = aStarSolver(maze, deepcopy(maze), [(1,1)], (random.choice(range(1,mazeSize-2,2)),random.choice(range(1,mazeSize-2,2))))
path = aStarSolver(maze, deepcopy(maze), [(1,1)], (mazeSize-2,mazeSize-2))

if path:
    for cell in path:
        maze[cell[0]][cell[1]] = '.'
    printMaze(maze)
else:
    print('Unsolvable')