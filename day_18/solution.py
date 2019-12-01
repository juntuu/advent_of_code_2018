
import curses
import time
from collections import Counter

with open('input.txt') as f:
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
	'''
	. -> | if | >= 3
	| -> # if # >= 3
	# -> . if # == 0 or | == 0
	'''
	new_yard = []
	for y, row in enumerate(yard):
		new_yard.append('')
		for x, current in enumerate(row):
			counts = adjacent(yard, x, y)
			if current == '.':
				if counts['|'] >= 3:
					current = '|'
			elif current == '|':
				if counts['#'] >= 3:
					current = '#'
			elif current == '#':
				if counts['#'] == 0 or counts['|'] == 0:
					current = '.'
			new_yard[-1] += current
	return new_yard


minutes = 10


def value(yard):
	counts = Counter(''.join(yard))
	return counts['#'] * counts['|']


def vis(scr):
	global yard
	curses.curs_set(False)
	for minute in range(minutes + 1):
		scr.clear()
		scr.addstr(0, 0, f'After {minute:2} minute{"" if minute == 1 else "s"}: {value(yard)}')
		for i, row in enumerate(yard):
			if i + 1 >= curses.LINES:
				break
			scr.addstr(i + 1, 0, row[:curses.COLS])

		scr.refresh()
		if minute == minutes:
			scr.addstr(1, 0, '<press any key to exit> ')
			scr.getkey()
			break
		yard = step(yard)
		time.sleep(0.5)


curses.wrapper(vis)
print('Day 18, part 1:', value(yard))

