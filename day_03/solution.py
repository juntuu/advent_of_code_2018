
from collections import namedtuple, Counter


class Claim(namedtuple('Claim', ['id', 'x', 'y', 'w', 'h'])):
	__slots__ = ()

	def __new__(cls, string):
		id, _, corner, dimensions = string.split()
		x, y = corner.split(',')
		w, h = dimensions.split('x')
		id = int(id[1:])
		x = int(x)
		y = int(y[:-1])
		w = int(w)
		h = int(h)
		return super().__new__(cls, id, x, y, w, h)

	def squares(self):
		return ((x, y)
			for x in range(self.x, self.x + self.w)
			for y in range(self.y, self.y + self.h))


with open('input.txt') as f:
	claims = [Claim(line) for line in f]

fabric = Counter()
for claim in claims:
	fabric.update(claim.squares())

overlap = sum(1 for v in fabric.values() if v > 1)
print('Day 3, part 1:', overlap)

