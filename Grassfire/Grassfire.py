import numpy as np
import math

PI = math.pi

class Grassfire:
    START = 0
    DEST = -1
    UNVIS = -2
    OBST = -3
    PATH = -4
    COLOR_START = np.array([0, 0.75, 0])
    COLOR_DEST = np.array([0.75, 0, 0])
    COLOR_UNVIS = np.array([1, 1, 1])
    COLOR_VIS = np.array([1, 0.5, 0.9])
    COLOR_OBST = np.array([0, 0, 0])
    COLOR_PATH = np.array([1, 1, 0])

    def random_grid(self, rows=16, cols=16, obstacleProb=0.3):
        '''Return a 2D numpy array representing a grid of randomly placed
        obstacles (where the likelihood of any cell being an obstacle
        is given by obstacleProb) and randomized start/destination cells.
        '''
        obstacleGrid = np.random.random_sample((rows, cols))
        grid = Grassfire.UNVIS * np.ones((rows, cols), dtype=np.int)
        grid[obstacleGrid <= obstacleProb] = self.OBST

        #prompts user to enter desired start and end position
        self.set_start_dest(grid)
        return grid

    def set_start_dest(self, grid):
        '''For a given grid, randomly select start and destination cells.'''
        (rows, cols) = grid.shape

        # Remove existing start and dest cells, if any.
        grid[grid == Grassfire.START] = Grassfire.UNVIS
        grid[grid == Grassfire.DEST] = Grassfire.UNVIS

        while (1):
            cho = input("Do you want to enter custom starting & goal position? Y/N::  ").upper()
            if cho == "Y" or cho == "YES":
                xAxis, yAxis = tuple(map(int, input('Please enter the starting position(x,y) separated by comma: ').split(',')))
                grid[xAxis,yAxis] = Grassfire.START
                xAxis, yAxis = tuple(map(int, input('Please enter the goal position(x,y) separated by comma: ').split(',')))
                grid[xAxis,yAxis] = Grassfire.DEST
                break;
            elif cho == "N" or cho == "NO":
                grid[0,0] = Grassfire.START
                grid[cols-1,rows-1] = Grassfire.DEST
                break;
            else:
                print("Oops! try again!")

    def color_grid(self, grid):
        '''Return MxNx3 pixel array ("color grid") corresponding to a grid.'''
        (rows, cols) = grid.shape
        colorGrid = np.zeros((rows, cols, 3), dtype=np.float)
        colorGrid[grid == Grassfire.OBST, :] = Grassfire.COLOR_OBST
        colorGrid[grid == Grassfire.UNVIS, :] = Grassfire.COLOR_UNVIS
        colorGrid[grid == Grassfire.START, :] = Grassfire.COLOR_START
        colorGrid[grid == Grassfire.DEST, :] = Grassfire.COLOR_DEST
        colorGrid[grid > Grassfire.START, :] = Grassfire.COLOR_VIS
        colorGrid[grid == Grassfire.PATH, :] = Grassfire.COLOR_PATH
        return colorGrid

    def reset_grid(self, grid):
        cellsToReset = ~((grid == Grassfire.OBST) + (grid == Grassfire.START)
            + (grid == Grassfire.DEST))
        grid[cellsToReset] = Grassfire.UNVIS

    def _check_adjacent(self, grid, cell, currentDepth):
        '''For given grid, check the cells adjacent to a given
            cell. If any have a depth (positive int) greater
            than the current depth, update them with the current
            depth, where depth represents distance from start cell.
            If destination found, return DEST constant; else, return
            number of adjacent cells updated.
        '''
        (rows, cols) = grid.shape
        numCellsUpdated = 0
        for i in range(4):
            rowToCheck = cell[0] + int(math.sin((PI/2) * i))
            colToCheck = cell[1] + int(math.cos((PI/2) * i))

            if not (0 <= rowToCheck < rows and 0 <= colToCheck < cols):
                continue
            elif grid[rowToCheck, colToCheck] == Grassfire.DEST:
                return Grassfire.DEST
            elif (grid[rowToCheck, colToCheck] == Grassfire.UNVIS
                or grid[rowToCheck, colToCheck] > currentDepth + 1):
                grid[rowToCheck, colToCheck] = currentDepth + 1
                numCellsUpdated += 1
        return numCellsUpdated

    def _backtrack(self, grid, cell, currentDepth):
        (rows, cols) = grid.shape
        for i in range(4):
            rowToCheck = cell[0] + int(math.sin((PI/2) * i))
            colToCheck = cell[1] + int(math.cos((PI/2) * i))
            if not (0 <= rowToCheck < rows and 0 <= colToCheck < cols):
                continue
            elif grid[rowToCheck, colToCheck] == currentDepth:
                nextCell = (rowToCheck, colToCheck)
                grid[nextCell] = Grassfire.PATH
                return nextCell

    def find_path(self, grid):
        nonlocalDict = {'grid': grid}
        def find_path_generator():
            grid = nonlocalDict['grid']
            depth = 0
            destFound = False
            cellsExhausted = False

            while (not destFound) and (not cellsExhausted):
                numCellsModified = 0
                depthIndices = np.where(grid == depth)
                matchingCells = list(zip(depthIndices[0], depthIndices[1]))

                for cell in matchingCells:
                    adjacentVal = self._check_adjacent(grid, cell, depth)
                    if adjacentVal == Grassfire.DEST:
                        destFound = True
                        break
                    else:
                        numCellsModified += adjacentVal

                if numCellsModified == 0:
                    cellsExhausted = True
                elif not destFound:
                    depth += 1
                yield

            if destFound:
                destCell = np.where(grid == Grassfire.DEST)
                backtrackCell = (destCell[0].item(), destCell[1].item())
                while depth > 0:
                    # Work backwards until return to start cell.
                    nextCell = self._backtrack(grid, backtrackCell, depth)
                    backtrackCell = nextCell
                    depth -= 1
                    yield
        return find_path_generator