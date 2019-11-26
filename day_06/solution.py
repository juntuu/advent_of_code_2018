
from collections import Counter

with open('input.txt') as f:
	points = [tuple(map(int, line.split(', '))) for line in f]

# points = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]


def manhattan_to(p0):
	x, y = p0
	return lambda p: abs(p[0] - x) + abs(p[1] - y)


xs, ys = zip(*points)
space = {}

# This happens to work on the specific input...
for x in range(min(xs), max(xs) + 1):
	for y in range(min(ys), max(ys) + 1):
		p = (x, y)
		a, b, *_ = sorted(points, key=manhattan_to(p))
		if manhattan_to(p)(a) != manhattan_to(p)(b):
			space[p] = a

point, count = Counter(space.values()).most_common(1)[0]
print('Day 6, part 1:', count)

