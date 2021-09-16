import curses
import sys
import time
from collections import Counter


def step(yard: list[str]):
	"""
	. -> | if | >= 3
	| -> # if # >= 3
	# -> . if # == 0 or | == 0
	"""

	def adjacent(x0: int, y0: int, what: str, limit: int):
		n = 0
		xs = slice(max(0, x0 - 1), x0 + 2)
		for r in yard[max(0, y0 - 1) : y0 + 2]:
			for c in r[xs]:
				if c in what:
					n += 1
					if n >= limit:
						return n

	def fn(x, y):
		current = yard[y][x]
		if current == ".":
			if adjacent(x, y, "|", 3):
				return "|"
		elif current == "|":
			if adjacent(x, y, "#", 3):
				return "#"
		elif current == "#":
			if not adjacent(x, y, "|", 1) or not adjacent(x, y, "#", 2):
				return "."
		return current

	r = range(len(yard))
	return ["".join(fn(x, y) for x in r) for y in r]


def run(yard: list[str]):
	n = Counter()
	max_n = 0
	cl = [0]
	values: list[int] = []
	for minute in range(more_minutes + 1):
		s = "".join(yard)
		if n[s] > max_n:
			if len(cl) > 1 and cl[-1] == cl[-2]:
				value_at_minutes = values[minutes]
				values = values[-cl[-1] :]
				diff = more_minutes - minute
				return value_at_minutes, values[diff % len(values)]
			max_n = n[s]
			cl.append(0)
		if n[s] == max_n:
			cl[-1] += 1
		n[s] += 1
		values.append(s.count("#") * s.count("|"))
		yield minute, yard, cl, values[-1]
		yard = step(yard)


def vis(scr):
	curses.curs_set(False)
	try:
		while True:
			minute, yard, lengths, value = next(gen)
			scr.clear()
			scr.addstr(
				0,
				0,
				f'After {minute:2} minute{"s" * (minute != 1)}: {value = }, cycle {lengths = }',
			)
			for i, row in enumerate(yard, 1):
				if i >= curses.LINES:
					break
				scr.addstr(i, 0, row[: curses.COLS])
			scr.refresh()
			time.sleep(0.1 if minute < minutes else 0.02)
	except StopIteration as res:
		values = res.args[0]
		s1 = f"found value at {more_minutes}: {values[1]}"
		s2 = "press any key to exit".ljust(len(s1))
		scr.addstr(1, 0, f"{s1} *  ")
		scr.addstr(2, 0, f"{s2} *  ")
		scr.addstr(3, 0, "*" * len(s1) + "**  ")
		scr.addstr(4, 0, " " * len(s1) + "    ")
		scr.refresh()
		scr.getkey()
		return values


with open("input.txt") as f:
	gen = run([row.strip() for row in f])

minutes = 10
more_minutes = 1000000000

if "-v" in sys.argv:
	value_at_minutes, value_at_more_minutes = curses.wrapper(vis)
else:
	try:
		while True:
			next(gen)
	except StopIteration as res:
		value_at_minutes, value_at_more_minutes = res.args[0]

print("Day 18, part 1:", value_at_minutes)
print("Day 18, part 2:", value_at_more_minutes)
