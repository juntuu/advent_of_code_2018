
from itertools import cycle


class Collision(Exception):
	def __init__(self, pos):
		self.pos = pos

	def __repr__(self):
		y, x = self.pos
		return f'Collision at: {x}{y}'


class Cart:
	positions = set()
	turn = '<v>^<^'
	corner = {
			'</': 'v',
			'^/': '>',
			'>/': '^',
			'v/': '<',
			'<\\': '^',
			'^\\': '<',
			'>\\': 'v',
			'v\\': '>',
			}

	def __init__(self, x, y, direction):
		self.turns = cycle((1, 0, -1))
		self.x = x
		self.y = y
		self.c = direction
		Cart.positions.add(self.position)

	def __repr__(self):
		return f'Cart({self.c}, {self.position})'

	def advance(self, track):
		Cart.positions.discard(self.position)
		if self.c == '<':
			self.x -= 1
		elif self.c == '>':
			self.x += 1
		elif self.c == '^':
			self.y -= 1
		elif self.c == 'v':
			self.y += 1
		at = track.get(self.position)
		if at == '+':
			self.c = Cart.turn[Cart.turn.find(self.c) + next(self.turns)]
		elif at:
			self.c = Cart.corner[self.c + at]
		if self.position in Cart.positions:
			raise Collision(self.position)
		Cart.positions.add(self.position)

	@property
	def position(self):
		return (self.y, self.x)

	def __lt__(self, other):
		x1, y1 = self.position
		x2, y2 = other.position
		return (y1, x1) < (y2, x2)


with open('input.txt') as f:
	track = {}
	carts = []
	for y, row in enumerate(f):
		for x, c in enumerate(row):
			if c in '<>^v':
				carts.append(Cart(x, y, c))
				continue
			elif c in r'\/+':
				track[(y, x)] = c


try:
	while True:
			carts.sort()
			for cart in carts:
				cart.advance(track)
except Collision as e:
	y, x = e.pos
	print(f'Day 13, part 1: {x},{y}')

