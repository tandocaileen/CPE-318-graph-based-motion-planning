import pygame
from info import BLACK, GREEN, RED, BG, OPENSET, CLOSEDSET, PATH
from info import GRIDSIZE, GRID_HEIGHT, GRID_WIDTH, SCREEN_HEIGHT

def drawRect(surface, point, colour):
	x, y = point
	r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
	pygame.draw.rect(surface, colour, r)
	pygame.draw.rect(surface, BLACK, r, 1)


def updateGrid(surface, openSet, closedSet, start, end):
	# Draw open and closed sets
	for node in openSet:
		drawRect(surface, node.pos, OPENSET)
	for node in closedSet:
		drawRect(surface, node.pos, CLOSEDSET)
	drawRect(surface, start, GREEN)
	drawRect(surface, end, RED)


def drawGrid(surface, maze, start, end):
	for x in range(int(GRID_WIDTH)):
		for y in range(int(GRID_HEIGHT)):
			if start and (x, y) == start:
				colour = GREEN
			elif end and (x, y) == end:
				colour = RED
			elif maze[x][y].obstacle:
				colour = BLACK
			else:
				colour = BG
			drawRect(surface, (x, y), colour)


def drawPath(surface, pathFound):
	pathFound = pathFound.parent
	while pathFound:
		if pathFound.parent:
			drawRect(surface, pathFound.pos, PATH)
		pathFound = pathFound.parent
