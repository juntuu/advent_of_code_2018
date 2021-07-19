from collections import namedtuple, defaultdict


class Claim(namedtuple("Claim", ["id", "x", "y", "w", "h"])):
	__slots__ = ()

	def __new__(cls, string):
		id, _, corner, dimensions = string.split()
		x, y = corner.split(",")
		w, h = dimensions.split("x")
		id = int(id[1:])
		x = int(x)
		y = int(y[:-1])
		w = int(w)
		h = int(h)
		return super().__new__(cls, id, x, y, w, h)

	def squares(self):
		return (
			(x, y)
			for x in range(self.x, self.x + self.w)
			for y in range(self.y, self.y + self.h)
		)


with open("input.txt") as f:
	claims = [Claim(line) for line in f]

fabric = defaultdict(set)
for claim in claims:
	for square in claim.squares():
		fabric[square].add(claim.id)

overlap = sum(1 for v in fabric.values() if len(v) > 1)
print("Day 3, part 1:", overlap)


all_claims = set(claim.id for claim in claims)

for made_claims in fabric.values():
	if len(made_claims) > 1:
		all_claims -= made_claims

assert len(all_claims) == 1
print("Day 3, part 2:", *all_claims)
