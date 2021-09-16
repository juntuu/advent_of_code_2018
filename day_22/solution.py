import heapq
import sys

from typing import NamedTuple, Callable, Iterable, TypeVar, Generic, Hashable


class GeoMap:
	def __init__(self, depth: int, target: tuple[int, int]):
		self.map = {(0, 0): 0, target: 0}
		self.depth = depth
		self.target = target
		self.max_x, self.max_y = target

	def __getitem__(self, i: tuple[int, int]):
		return self.erosion(i) % 3

	def as_grid(self):
		return [
			[self[x, y] for x in range(self.max_x + 1)] for y in range(self.max_y + 1)
		]

	def erosion(self, i: tuple[int, int]):
		if i not in self.map:
			x, y = i
			self.max_x = max(x, self.max_x)
			self.max_y = max(y, self.max_y)
			if y == 0:
				self.map[i] = x * 16807
			elif x == 0:
				self.map[i] = y * 48271
			else:
				self.map[i] = self.erosion((x - 1, y)) * self.erosion((x, y - 1))
		return (self.map[i] + self.depth) % 20183


T = TypeVar("T", bound=Hashable)
K = TypeVar("K")


class PriorityQ(Generic[T, K]):
	def __init__(self, it: Iterable[T], *, key: Callable[[T], K]):
		self.set = set(it)
		self.key = key
		self.list = [(key(e), e) for e in self.set]
		heapq.heapify(self.list)

	def __bool__(self):
		return bool(self.set)

	def __len__(self):
		return len(self.set)

	def pop(self):
		while self.set:
			item = heapq.heappop(self.list)[1]
			if item in self.set:
				self.set.remove(item)
				return item
		raise KeyError("pop from an empty queue")

	def push(self, item: T):
		self.set.add(item)
		heapq.heappush(self.list, (self.key(item), item))


class Node(NamedTuple):
	x: int
	y: int
	gear: str


# A* from wikipedia:
# see https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
def a_star(
	start: T,
	goal: T,
	h: Callable[[T], int],
	edges: Callable[[T], Iterable[tuple[T, int]]],
):
	came_from: dict[T, T] = {}
	g_score = {start: 0}
	f_score = {start: h(start)}

	open_set = PriorityQ([start], key=f_score.__getitem__)
	while open_set:
		current = open_set.pop()
		if current == goal:
			path = [current]
			while current in came_from:
				current = came_from[current]
				path.append(current)
			return g_score[goal], reversed(path)

		current_score = g_score[current]
		for neighbor, distance in edges(current):
			tentative_g_score = current_score + distance
			if tentative_g_score < g_score.get(neighbor, tentative_g_score + 1):
				came_from[neighbor] = current
				g_score[neighbor] = tentative_g_score
				f_score[neighbor] = tentative_g_score + h(neighbor)
				open_set.push(neighbor)
	assert False, "no path"


def heuristic(node: Node):
	return abs(node.x - x) + abs(node.y - y) + 7


def neighbors(node: Node):
	valid_gear = ["torch", "climbing", "neither", "torch"]
	x, y, gear = node
	region = geo_map[x, y]
	for tool in valid_gear[region : region + 2]:
		if tool != gear:
			yield node._replace(gear=tool), 7
	for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
		xi, yi = x + dx, y + dy
		if xi < 0 or yi < 0:
			continue
		region = geo_map[xi, yi]
		if gear in valid_gear[region : region + 2]:
			yield Node(xi, yi, gear), 1


def print_path(path):
	chars = {
		0: " .",
		1: " =",
		2: " |",
		"torch": "T",
		"climbing": "C",
		"neither": "N",
	}
	grid = [[list(chars[c]) for c in row] for row in geo_map.as_grid()]
	grid[0][0].append("S")

	max_x = max_y = 0
	for xi, yi, tool in path:
		max_x = max(max_x, xi)
		max_y = max(max_y, yi)
		grid[yi][xi].append(chars[tool])

	grid[y][x].append("G")
	for row in grid[: max_y + 1]:
		print("".join("".join(e[-2:]) for e in row[: max_x + 1]))


x = 10
y = 715

geo_map = GeoMap(3339, (x, y))

total = sum(geo_map[i, j] for i in range(x + 1) for j in range(y + 1))
print("Day 22, part 1: ", total)

cost, path = a_star(Node(0, 0, "torch"), Node(x, y, "torch"), heuristic, neighbors)
if "--path" in sys.argv:
	print_path(path)
print("Day 22, part 2: ", cost)
