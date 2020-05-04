from collections import namedtuple
import heapq
import re


Bot = namedtuple("Bot", ["x", "y", "z", "r"])

# pos=<0,0,0>, r=4
number = re.compile(r"-?\d+")
with open("input.txt") as f:
	nanobots = [Bot(*map(int, number.findall(line))) for line in f]


def manhattan(a, b=(0, 0, 0), d=3):
	return sum(abs(i - j) for i, j in zip(a[:d], b[:d]))


max_bot = max(nanobots, key=lambda b: b.r)
in_range = sum(manhattan(max_bot, bot) <= max_bot.r for bot in nanobots)

print("Day 23, part 1:", in_range)


def intersects(cube: Bot, bot: Bot):
	d = sum(
		abs(b - (a - cube.r)) + abs(b - (a - 1 + cube.r))
		for a, b in zip(cube[:3], bot[:3])
	)
	return d // 2 < bot.r + 3 * cube.r


def countbots(cube: Bot):
	return sum(intersects(cube, bot) for bot in nanobots)


R = Bot(0, 0, 0, 8)
while countbots(R) < len(nanobots):
	R = R._replace(r=R.r * 2)


def divide(cube: Bot):
	x, y, z, r = cube
	r //= 2
	return [
		Bot(x - r, y - r, z - r, r),
		Bot(x - r, y - r, z + r, r),
		Bot(x - r, y + r, z - r, r),
		Bot(x - r, y + r, z + r, r),
		Bot(x + r, y - r, z - r, r),
		Bot(x + r, y - r, z + r, r),
		Bot(x + r, y + r, z - r, r),
		Bot(x + r, y + r, z + r, r),
	]


def search():
	q = [(0, 0, 0, R)]
	while q:
		*_, d, r0 = heapq.heappop(q)
		if r0.r == 1:
			return d
		for r in divide(r0):
			heapq.heappush(q, (-countbots(r), -r.r, manhattan(r), r))


distance = search()
print("Day 23, part 2:", distance)
