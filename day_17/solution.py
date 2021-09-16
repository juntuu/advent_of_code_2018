import curses
import time
import sys

example = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""


def read_veins(lines):
	for line in lines:
		a, b = line.split(", ")
		mark, a = a.split("=")
		a1 = int(a)
		b1, b2 = map(int, b[2:].split(".."))
		if mark == "x":
			for y in range(b1, b2 + 1):
				yield a1, y
		else:
			for x in range(b1, b2 + 1):
				yield x, a1


def spread(x, y, stack):
	a = False
	b = False
	for lx in range(x, min_x - 2, -1):
		if not ((lx, y + 1) in clay or (lx, y + 1) in water):
			break
		if (lx, y) in clay:
			a = True
			break
	for rx in range(x, max_x + 1):
		if not ((rx, y + 1) in clay or (rx, y + 1) in water):
			break
		if (rx, y) in clay:
			b = True
			break
	yield lx + 1, y, "|~"[a and b] * (rx - lx - 1)
	(water if a and b else wet).update((xi, y) for xi in range(lx + 1, rx))
	if lx == rx:
		return
	if not a:
		stack.append((lx, y - 1))
	if not b:
		stack.append((rx, y - 1))


def flow():
	stack = [spring]
	while stack:
		x, y = stack.pop()
		if y >= max_y:
			continue
		yield x, y, None

		pos = x, y + 1
		while y < max_y and pos not in wet and pos not in clay and pos not in water:
			y += 1
			yield x, y, "|"
			if y >= min_y:
				wet.add(pos)
			stack.append(pos)
			pos = x, y + 1

		yield from spread(x, y, stack)


def vis(scr):
	scr.clear()
	pad = curses.newpad(max_y + curses.LINES + 2, max_x + curses.COLS + 2)
	for x, y in clay:
		pad.addch(y, x, "#")
	pad.addch(spring[1], spring[0], "+")
	dx = curses.COLS // 2
	dy = curses.LINES // 2
	cx, cy = spring
	cx -= dx
	pad.nodelay(True)
	for x, y, c in stream:
		if c:
			pad.addstr(y, x, c)
		pad.move(y, x)
		if abs(x - (cx + dx)) > dx - 4:
			cx = max(0, x - dx)
		if abs(y - (cy + dy)) > dy - 4:
			cy = max(0, y - dy)
		pad.refresh(cy, cx, 0, 0, curses.LINES - 1, curses.COLS - 1)
		if pad.getch() == ord("q"):
			return
		time.sleep(0.01)
	pad.nodelay(False)
	pad.getkey()


with open("input.txt") as f:
	clay = set(read_veins(line.strip() for line in f))

spring = (500, 0)
(min_x, _), *_, (max_x, _) = sorted(clay)
(_, min_y), *_, (_, max_y) = sorted(clay, key=lambda p: p[1])
wet = set()
water = set()
stream = flow()

if "-v" in sys.argv:
	curses.wrapper(vis)

for _ in stream:
	pass

total_wet = sum(min_y <= y <= max_y for _, y in wet | water)
print("Day 17, part 1:", total_wet)

total_water = sum(min_y <= y <= max_y for _, y in water)
print("Day 17, part 2:", total_water)
