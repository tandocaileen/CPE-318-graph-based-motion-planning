import numpy as np
from heapq import heappush, heappop
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
a = []
b = []
path_len = 0

def update_points(num):
    point_ani.set_data(a[num], b[num])
    xdata.append(a[num])
    ydata.append(b[num])
    if num % path_len == 0:
        xdata.clear()
        ydata.clear()
    point_ani.set_data(ydata, xdata)
    return point_ani,

def heuristic_cost_estimate(neighbor, goal):
    x = neighbor[0] - goal[0]
    y = neighbor[1] - goal[1]
    return abs(x) + abs(y)

def dist_between(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path


def astar(array, start, goal):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),] # 8 directions ,(1, 1), (1, -1), (-1, 1), (-1, -1)
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic_cost_estimate(start, goal)}

    openSet = []
    heappush(openSet, (fscore[start], start))

    while openSet:
        current = heappop(openSet)[1]
        if current == goal:
            return reconstruct_path(came_from, current)
        close_set.add(current)

        for i, j in directions:  #  Check the 8 adjacent nodes of the current node one by one
            neighbor = current[0] + i, current[1] + j

            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 30:  #  1 is obstacle
                        continue
                else:
                    # array bounded in y walls
                    continue
            else:
                # array bounded in x walls
                continue

            # Ignore neighbor which is already evaluated.
            if neighbor in close_set:
                continue

            #  The distance from start to a neighbor via current
            tentative_gScore = gscore[current] + dist_between(current, neighbor)

            if neighbor not in [i[1] for i in openSet]:
                heappush(openSet, (fscore.get(neighbor, np.inf), neighbor))
            elif tentative_gScore >= gscore.get(neighbor, np.inf):
                continue

            came_from[neighbor] = current
            gscore[neighbor] = tentative_gScore
            fscore[neighbor] = tentative_gScore + heuristic_cost_estimate(neighbor, goal)
    return False

if __name__ == "__main__":
    while 1:
        cho = input("Do you want to enter custom grid size? Y/N::  ").upper()
        if cho=="Y" or cho=="YES":
            mapsize = tuple(map(int, input('Please enter the grid size(x,y) separated by comma: ').split(',')))
            break
        elif cho=="N" or cho=="NO":
            mapsize = (10,10)
            break
        else:
            print("Oops! try again!")

    nmap = np.zeros(mapsize)
    map_weight = nmap.shape[0]
    map_height = nmap.shape[1]
    obs = []

    while 1:
        cho = input("\nDo you want to enter starting and goal position? Y/N::  ").upper()
        if cho == "Y" or cho == "YES":
            starter = tuple(map(int, input('Please enter the starting position(x,y) separated by comma: ').split(',')))
            goalie = tuple(map(int, input('Please enter the goal position(x,y) separated by comma: ').split(',')))
            break
        elif cho == "N" or cho == "NO":
            starter = (0, 0)
            goalie = (nmap.shape[0] - 1, nmap.shape[0] - 1)
            break
        else:
            print("Oops! try again!")

    start_node = (starter[0],starter[1])
    end_node = (goalie[0],goalie[1])

    while 1:
        cho = input("\nDo you want to enter custom obstacles? Y/N::  ").upper()
        if cho == "Y" or cho == "YES":
            obsNum = int(input("Enter number of obstacles:: "))
            for i in range(obsNum):
                print("Obstacle", i+1)
                xi, yi = map(int, input('Please enter the obstacle position(x,y) separated by comma: ').split(','))
                nmap[yi][xi] = 30
            break
        elif cho == "N" or cho == "NO":
            #  Random generate grid
            for i in range(int(0.30 * map_weight * map_height)):
                xi = random.randint(0, map_weight - 1)
                yi = random.randint(0, map_height - 1)
                nmap[xi][yi] = 30
            break
        else:
            print("Oops! try again!")

    nmap[start_node] = 0
    nmap[end_node] = 0

    path = astar(nmap, end_node, start_node) # with a star algorithm generating path
    path_len = len(path)
    for i in range(path_len):
        nmap[path[i]] = 80
        a.append(path[i][0])
        b.append(path[i][1])

    nmap[start_node] = 145
    nmap[end_node] = 185
    img = np.array(nmap)

xdata = []
ydata = []
fig = plt.figure()
point_ani = plt.axes(xlim=(-1, mapsize[1]), ylim=(-1, mapsize[0]))
point_ani, = plt.plot(xdata, ydata, "*w")
im = plt.imshow(img)
ani = animation.FuncAnimation(fig, update_points, np.arange(0,len(a)-1), interval=100, blit=True)
plt.title("A* Pathfinding ")
plt.show()
