import curses
import time
from collections import Counter

with open("input.txt") as f:
	yard = [row.strip() for row in f]


def adjacent(yard, x0, y0):
	counts = Counter()
	r = range(-1, 2)
	for dx, dy in ((i, j) for i in r for j in r if i or j):
		y = y0 + dy
		x = x0 + dx
		if 0 <= y < len(yard) and 0 <= x < len(yard[0]):
			counts[yard[y][x]] += 1
	return counts


def step(yard):
	"""
	. -> | if | >= 3
	| -> # if # >= 3
	# -> . if # == 0 or | == 0
	"""
	new_yard = []
	for y, row in enumerate(yard):
		new_yard.append("")
		for x, current in enumerate(row):
			counts = adjacent(yard, x, y)
			if current == ".":
				if counts["|"] >= 3:
					current = "|"
			elif current == "|":
				if counts["#"] >= 3:
					current = "#"
			elif current == "#":
				if counts["#"] == 0 or counts["|"] == 0:
					current = "."
			new_yard[-1] += current
	return new_yard


minutes = 10
more_minutes = 1000000000
value_at_minutes = None
value_at_more_minutes = None


def value(yard):
	counts = Counter("".join(yard))
	return counts["#"] * counts["|"]


def vis(scr):
	global yard
	global value_at_minutes
	global value_at_more_minutes
	curses.curs_set(False)
	n = Counter()
	max_n = 0
	cl = [0]
	values = []
	for minute in range(more_minutes + 1):
		s = "".join(yard)
		if n[s] > max_n:
			if len(cl) > 1 and cl[-1] == cl[-2]:
				values = values[-cl[-1] :]
				diff = more_minutes - minute
				value_at_more_minutes = values[diff % len(values)]
			max_n = n[s]
			cl.append(0)
		if n[s] == max_n:
			cl[-1] += 1
		n[s] += 1
		values.append(value(yard))
		if minute == minutes:
			value_at_minutes = values[-1]

		if minute <= minutes:
			time.sleep(0.2)
		if minute % 4 == 0 or minute < minutes or n.most_common(1)[0][1] > 1:
			scr.clear()
			scr.addstr(
				0,
				0,
				f'After {minute:2} minute{"" if minute == 1 else "s"}: value = {value(yard)}, cycle lengths = {cl}',
			)
			for i, row in enumerate(yard):
				if i + 1 >= curses.LINES:
					break
				scr.addstr(i + 1, 0, row[: curses.COLS])
			scr.refresh()

		if value_at_more_minutes is not None:
			s1 = f"found value at {more_minutes}: {value_at_more_minutes}"
			s2 = "press any key to exit"
			length = max(len(s1), len(s2))
			scr.addstr(1, 0, f"{s1.ljust(length)} *  ")
			scr.addstr(2, 0, f"{s2.ljust(length)} *  ")
			scr.addstr(3, 0, "*" * length + "**  ")
			scr.addstr(4, 0, " " * length + "    ")
			scr.refresh()
			scr.getkey()
			break

		yard = step(yard)


try:
	curses.wrapper(vis)
except KeyboardInterrupt:
	pass

if value_at_minutes is not None:
	print("Day 18, part 1:", value_at_minutes)
if value_at_more_minutes is not None:
	print("Day 18, part 2:", value_at_more_minutes)
