
from collections import namedtuple, defaultdict
import math
import heapq


class GeoMap:
	def __init__(self, depth, target):
		self.map = {(0, 0): 0, target: 0}
		self.depth = depth
		self.target = target

	def __getitem__(self, i):
		return self.erosion(i) % 3

	def erosion(self, i):
		if i not in self.map:
			x, y = i
			if y == 0:
				self.map[i] = x * 16807
			elif x == 0:
				self.map[i] = y * 48271
			else:
				self.map[i] = self.erosion((x - 1, y)) * self.erosion((x, y - 1))
		return (self.map[i] + self.depth) % 20183


depth = 3339
x = 10
y = 715

geo_map = GeoMap(depth, (x, y))
total = sum(geo_map[i, j] for i in range(x + 1) for j in range(y + 1))
print("Day 22, part 1: ", total)


class PriorityQ:
	def __init__(self, it, *, key=lambda x: x):
		self.set = set(it)
		self.key = key
		self.list = list((key(e), e) for e in self.set)
		heapq.heapify(self.list)

	def __bool__(self):
		return bool(self.set)

	def __len__(self):
		return len(self.set)

	def pop(self):
		while self.set:
			item = heapq.heappop(self.list)[1]
			if item in self.set:
				self.set.discard(item)
				return item
		raise KeyError('pop from an empty queue')

	def push(self, item):
		self.set.add(item)
		heapq.heappush(self.list, (self.key(item), item))


# A* from wikipedia:
# see https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
def a_star(start, goal, h, neighbors):
	came_from = {}
	g_score = defaultdict(lambda: math.inf)
	g_score[start] = 0

	f_score = defaultdict(lambda: math.inf)
	f_score[start] = h(start)

	open_set = PriorityQ([start], key=lambda p: f_score[p])
	while open_set:
		current = open_set.pop()
		if current == goal:
			path = [current]
			while current in came_from:
				current = came_from[current]
				path.append(current)
			return g_score[goal], reversed(path)

		for neighbor, distance in neighbors(current):
			tentative_g_score = g_score[current] + distance
			if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = tentative_g_score
				f_score[neighbor] = g_score[neighbor] + h(neighbor)
				open_set.push(neighbor)


Node = namedtuple('Node', ['x', 'y', 'gear'])
start = Node(0, 0, 'torch')
goal = Node(x, y, 'torch')


def heuristic(node):
	return abs(node.x - goal.x) + abs(node.y - goal.y) + 7


def neighbors(node):
	valid_gear = ['torch', 'climbing', 'neither', 'torch']
	x, y, gear = node
	region = geo_map[x, y]
	for tool in valid_gear[region:region+2]:
		if tool != gear:
			yield node._replace(gear=tool), 7
	for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
		xi, yi = x + dx, y + dy
		if xi < 0 or yi < 0:
			continue
		region = geo_map[xi, yi]
		if gear in valid_gear[region:region+2]:
			yield Node(xi, yi, gear), 1


cost, path = a_star(start, goal, heuristic, neighbors)
print("Day 22, part 2: ", cost)

