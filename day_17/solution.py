import curses
import time

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
	veins = set()
	for line in lines:
		a, b = line.split(", ")
		mark, a = a.split("=")
		a1 = int(a)
		b1, b2 = map(int, b[2:].split(".."))
		if mark == "x":
			for y in range(b1, b2 + 1):
				veins.add((a1, y))
		else:
			for x in range(b1, b2 + 1):
				veins.add((x, a1))
	return veins


# clay = read_veins(example.strip().splitlines())
with open("input.txt") as f:
	clay = read_veins(line.strip() for line in f)

spring = (500, 0)
(min_x, _), *_, (max_x, _) = sorted(clay)
(_, min_y), *_, (_, max_y) = sorted(clay, key=lambda p: p[1])
wet = set()
water = set()


def spread(x, y, stack):
	a = False
	b = False
	for lx in range(x, min_x - 2, -1):
		if (lx, y + 1) not in clay | water:
			break
		if (lx, y) in clay:
			a = True
			break
	for rx in range(x, max_x + 1):
		if (rx, y + 1) not in clay | water:
			break
		if (rx, y) in clay:
			b = True
			break
	if a and b:
		yield (lx + 1, y, "~" * (rx - lx - 1))
	else:
		yield (lx + 1, y, "|" * (rx - lx - 1))
	for xi in range(lx + 1, rx):
		pos = (xi, y)
		if a and b:
			water.add(pos)
		else:
			wet.add(pos)
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
		yield (x, y, None)

		while y < max_y and (x, y + 1) not in wet | water | clay:
			y += 1
			yield (x, y, "|")
			if y >= min_y:
				wet.add((x, y))
			stack.append((x, y))

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
	for i, (x, y, c) in enumerate(flow()):
		if c:
			pad.addstr(y, x, c)
		pad.move(y, x)
		if abs(x - (cx + dx)) > dx - 4:
			cx = max(0, x - dx)
		if abs(y - (cy + dy)) > dy - 4:
			cy = max(0, y - dy)
		pad.refresh(cy, cx, 0, 0, curses.LINES - 1, curses.COLS - 1)
		# time.sleep(0.1)
	pad.getkey()


try:
	curses.wrapper(vis)
except KeyboardInterrupt:
	print("bye.")
	exit(0)

# for _ in flow(): pass

total_wet = sum(1 for (_, y) in wet | water if min_y <= y <= max_y)
print("Day 17, part 1:", total_wet)

total_water = sum(1 for (_, y) in water if min_y <= y <= max_y)
print("Day 17, part 2:", total_water)
