import pygame
from queue import PriorityQueue
class Node:
    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white  # Default color for each square
        self.neighbors = []
        self.width = width
        self.totalRows = totalRows

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Checks if the nodes are barriers and if they are not we will add it to the neighbors list
    def updateNodeNeighbors(self, grid):
        self.neighbors = []
        # Checking if we can move down a square
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].nodeBarrier():
            self.neighbors.append(grid[self.row + 1][self.col])  # Append the next row

        # Checking if we can move up a square
        if self.row > 0 and not grid[self.row - 1][self.col].nodeBarrier():
            self.neighbors.append(grid[self.row - 1][self.col])  # Append the next row

        # Checking if we can move to the right of a square
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].nodeBarrier():
            self.neighbors.append(grid[self.row][self.col + 1])  # Append the next row

        # Checking if we can move to the left of a square
        if self.col > 0 and not grid[self.row][self.col - 1].nodeBarrier():
            self.neighbors.append(grid[self.row][self.col - 1])  # Append the next row

    # Comparison
    def __lt__(self, other):
        return False

    def nodeClosed(self):
        return self.color == red
    def getPosition(self):
        return self.row, self.col
    def nodeBarrier(self):
        return self.color == black
    def nodeOpen(self):
        return self.color == green
    def nodeEnd(self):
        return self.color == pink
    def nodeStart(self):
        return self.color == blue
    def nodeReset(self):
        self.color = white
    def makeNodeClosed(self):
        self.color = red
    def makeNodeStart(self):
        self.color = blue
    def makeNodeOpen(self):
        self.color = green
    def makeBarrier(self):
        self.color = black
    def makeEnd(self):
        self.color = pink
    def makePath(self):
        self.color = purple

def hFunction(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)  # Returing the absolute value


# This function reconstructs the path from the start node to the end node once the algorithm is completed
def reconstructPath(cameFrom, current, draw):
    while current in cameFrom:
        current = cameFrom[current]
        current.makePath()
        draw()

# Algorithm function
def algorithm(draw, grid, start, end):
    count = 0
    openset = PriorityQueue()

    openset.put((0, count, start))  # start = node, count = any number, 0 = f score which is zero
    cameFrom = {}
    gScore = {spot: float("inf") for row in grid for spot in row}  # Keeps track of the current shortest distance
    gScore[start] = 0  # Gscore for start node is zero
    fScore = {spot: float("inf") for row in grid for spot in
              row}  # Keeps track of the predicted distance from the current node to the end node
    fScore[start] = hFunction(start.getPosition(), end.getPosition())  # Value is whatever the heuristic distance is

    openset_hash = {start}  # Helps us see if something is in the openset

    while not openset.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = openset.get()[2]  # We just want node so we grab that at the second index
        openset_hash.remove(current)  # Remove the current node to avoid duplicates

        # If the current node is the end node then the following will occur
        if current == end:
            reconstructPath(cameFrom, end, draw)  # Reconstructing the path from the start node to the end node
            end.makeEnd()
            start.makeNodeStart()
            return True

        for neighbor in current.neighbors:
            tempGScore = gScore[current] + 1
            # If we found a better path to the end node then update the value
            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + hFunction(neighbor.getPosition(), end.getPosition())
                if neighbor not in openset_hash:
                    count += 1
                    openset.put((fScore[neighbor], count, neighbor))
                    openset_hash.add(neighbor)
                    neighbor.makeNodeOpen()

        draw()  # Calling the draw function to run (passed in through lambda (anonymous function))

        if current != start:
            current.makeNodeClosed()

    return False  # Returing false if we could not find a path

def dGrid(rows, width):
    grid = []
    gapBetweenRows = width // rows
    for row in range(rows):
        grid.append([])
        for col in range(rows):
            node = Node(row, col, gapBetweenRows, rows)  # Making an object of the Node class and passing in the values
            grid[row].append(node)
    return grid

def gridLines(win, rows, width):
    gap = width // rows
    # Making the horizontal gridlines
    for row in range(rows):
        pygame.draw.line(win, grey, (0, row * gap), (width, row * gap))
        # Making the vertical gridlines
        for col in range(rows):
            pygame.draw.line(win, grey, (col * gap, 0), (col * gap, width))


# Drawing everything
def draw(win, grid, rows, width):
    win.fill(white)  # Fill everything in white
    for row in grid:
        for node in row:
            node.draw(win)
    # Drawing gridlines on top of the filled squres
    gridLines(win, rows, width)
    pygame.display.update()  # Updating the display


# Takes mouse position and determines which node is clicked
def getClickedPosition(position, rows, width):
    gap = width // rows
    y, x = position

    # Tells us where we are
    row = y // gap
    col = x // gap

    return row, col  # Returing the row and column that was clicked


# Main function
def main(win, width):
    rows = int(input("Enter Grid size (square):: "))
    print("***************INSTRUCTIONS***************\n"
          "1. Click the starting position. (blue)\n"
          "2. Click the goal position. (pink)\n"
          "3. CLick anywhere for the obstacles. (black)\n"
          "4. Press enter on your keyboard to solve.(violet)")
    grid = dGrid(rows, width)  # Generating the grid (2D list of spots)
    start = None
    end = None
    run = True

    while run:
        draw(win, grid, rows, width)
        # At the beginning of the event lets check each event in pygame by iterating through them
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Checking mouse positions
            # If the user presses the left mouse button
            if pygame.mouse.get_pressed()[0]:

                position = pygame.mouse.get_pos()
                row, col = getClickedPosition(position, rows, width)
                spot = grid[row][col]

                # Placing the start position first (if it is not placed already)
                if not start and spot != end:
                    start = spot
                    start.makeNodeStart()
                # Placing the end position second (if it is not placed already)
                elif not end and spot != start:
                    end = spot
                    end.makeEnd()
                # If the start and end position are placed then make barrier cubes
                elif spot != start and spot != end:
                    spot.makeBarrier()
            # If the user presses the right mouse button
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, col = getClickedPosition(position, rows, width)
                spot = grid[row][col]
                spot.nodeReset()
                # Resetting the start and end if they are pressed
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            # If a key is pressed on the keyboard
            if event.type == pygame.KEYDOWN:
                # If the user presses the enter button the algorithm will start
                if event.key == pygame.K_RETURN and start and end:
                    for row in grid:
                        for spot in row:
                            spot.updateNodeNeighbors(grid)

                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)  # Calling the algorithm function
                if event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = dGrid(rows, width)
    pygame.quit()  # Quitting pygame

width = 600
window = pygame.display.set_mode((width, width))
red = (224,24,3)
green = (3,224,162)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (122,3,224)
blue = (100,149,237)
grey = (128, 128, 128)
pink = (254,130,172)
pygame.display.set_caption("A* PathFinding Algorithm")
main(window, width)  # Calling the main function to run the program