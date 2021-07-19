from itertools import cycle


class Collision(Exception):
	def __init__(self, pos, *carts):
		self.pos = pos
		self.carts = carts

	def __repr__(self):
		y, x = self.pos
		return f"Collision at: {x}{y}"


class Cart:
	positions = {}
	turn = "<v>^<^"
	corner = {
		"</": "v",
		"^/": ">",
		">/": "^",
		"v/": "<",
		"<\\": "^",
		"^\\": "<",
		">\\": "v",
		"v\\": ">",
	}

	def __init__(self, x, y, direction):
		self.turns = cycle((1, 0, -1))
		self.x = x
		self.y = y
		self.c = direction
		Cart.positions[self.position] = self

	def __repr__(self):
		return f"Cart({self.c}, {self.position})"

	def advance(self, track):
		Cart.positions.pop(self.position, None)
		if self.c == "<":
			self.x -= 1
		elif self.c == ">":
			self.x += 1
		elif self.c == "^":
			self.y -= 1
		elif self.c == "v":
			self.y += 1
		at = track.get(self.position)
		if at == "+":
			self.c = Cart.turn[Cart.turn.find(self.c) + next(self.turns)]
		elif at:
			self.c = Cart.corner[self.c + at]
		other = Cart.positions.get(self.position)
		if other is not None:
			Cart.positions.pop(self.position)
			raise Collision(self.position, self, other)
		Cart.positions[self.position] = self

	@property
	def position(self):
		return (self.y, self.x)

	def __lt__(self, other):
		x1, y1 = self.position
		x2, y2 = other.position
		return (y1, x1) < (y2, x2)


with open("input.txt") as f:
	track = {}
	carts = []
	for y, row in enumerate(f):
		for x, c in enumerate(row):
			if c in "<>^v":
				carts.append(Cart(x, y, c))
				continue
			elif c in r"\/+":
				track[(y, x)] = c


first = True
while carts:
	if len(carts) == 1:
		y, x = carts[0].position
		print(f"Day 13, part 2: {x},{y}")
		break
	carts.sort()
	i = 0
	while i < len(carts):
		try:
			carts[i].advance(track)
			i += 1
		except Collision as e:
			y, x = e.pos
			for cart in e.carts:
				j = carts.index(cart)
				if j < i:
					i -= 1
				carts.pop(j)
			if first:
				print(f"Day 13, part 1: {x},{y}")
				first = False
