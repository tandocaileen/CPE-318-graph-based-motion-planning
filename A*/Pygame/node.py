from math import sqrt
from info import GRID_WIDTH, GRID_HEIGHT, DIRECTIONS
import random

class Node(object):
	f = 0
	g = 0
	h = 0
	parent = None
	obstacle = False

	def __init__(self, pos, obstacle=0):
		if (random.randrange(10)/10) < obstacle:
			self.obstacle = True
		self.pos = pos

	def heuristic(self, point, taxi=False):
		x, y = self.pos
		xp, yp = point

		delta_x = xp - x
		delta_y = yp - y
		
		# Taxi or Euclidian distance
		if taxi:
			self.h = abs(delta_x) + abs(delta_y)
		else:
			self.h = sqrt((delta_x**2)+(delta_y**2))

	def update(self, g, end, parent, taxi):
		self.parent = parent
		self.g = g
		self.heuristic(end, taxi)
		self.f = self.g + self.h
	
	def getG(self, point):
		x, y = point
		x2, y2 = self.pos
		if abs((x-x2)) + abs((y-y2)) == 2:
			return 1.41
		return 1

	def _sumPoints(self, a, b):
		xa, ya = a
		xb, yb = b
		return (xa+xb, ya+yb)

	def _outofbounds(self, point):
		x, y = point
		if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
			return True
		return False

	def getNeighbours(self, maze):
		neighbours = []
		for dir in DIRECTIONS:
			x, y = self._sumPoints(self.pos, dir)
			if not self._outofbounds((x, y)) and not maze[x][y].obstacle:
				neighbours.append(maze[x][y])
		return neighbours

	def printInfo(self):
		print(self.pos)
		if self.parent:
			print(f"parent: {self.parent.pos}")
		else:
			print(f"parent: {self.parent}")
		print(f"f:{self.f} = g:{self.g} + h:{self.h}\n")
