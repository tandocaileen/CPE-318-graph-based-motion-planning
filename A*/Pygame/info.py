print("******************************************************************\n"
      "                            INPUT HERE\n"
      "******************************************************************")
while True:
    cho = input("Do you want to customize grid size? Y/N ::  ").upper()
    if cho == "Y" or cho=="YES":
        gr = int(input("Enter grid size (square)::  "))
        break;
    elif cho == "N" or cho== "NO":
        gr = 10
        break
    else:
        print("oops! try again!")


print('******************************************************************\n'
      '                           INSTRUCTIONS\n'
      '******************************************************************\n'
      '- Left click the starting position.\n'
	  '- Right click the goal position\n'
      '- Press the 0 key while hovering to the box you want to set as obstacle\n'
	  '- Press enter key to find path\n'
	  '- Press any of 1-6 (1 being the least while 6 being the most dense) key to randomize obstacles\n'
	  '- Press space key to clear the grid\n'
      '- Press t key to switch between euclidian(8 directions) or taxicab geometry (4 directions)\n'
	  '- Press arrows up or down to speed up or slow down the animation.\n'
	  '- Press r key to use fixed start and goal positions\n'
	  'NOW PRESS OK AND MANUALLY OPEN THE PYGAME WINDOW :D')


GRIDSIZE = int(600/gr)
graw = 600/gr
GRID_WIDTH = int(600 / GRIDSIZE)
GRID_HEIGHT = int(600 / GRIDSIZE)
w =  600 / GRIDSIZE
SCREEN_WIDTH = (600*2)-(w*graw)
SCREEN_HEIGHT = (600*2)-(w*graw)

RIGHT_CLICK = (False, False, False)
LEFT_CLICK = (True, False, False)
EYYY = (False, False, True)

UP = (0, -1)
UPRIGHT = (1, -1)
UPLEFT = (-1, -1)
DOWN = (0, 1)
DOWNRIGHT = (1, 1)
DOWNLEFT = (-1, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = [UP, UPRIGHT, RIGHT, DOWNRIGHT, DOWN, DOWNLEFT, LEFT, UPLEFT]

BLACK = (0,0,0)
WHITE = (255,255,255)
BG = (210,200,200)
RED = (150,0,0)
GREEN = (0,150,0)
BLUE = (0,0,100)
PATH = (50,50,200)
OPENSET = (255,180,100)
CLOSEDSET = (255,100,100)