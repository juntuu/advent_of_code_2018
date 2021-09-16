class Unit(str):
	hp = 200
	ap = 3


class Elf(Unit):
	def __new__(cls, ap):
		e = super().__new__(cls, "E")
		e.ap = ap
		return e

	def __setattr__(self, key, val):
		if key == "hp" and val <= 0:
			raise ValueError("dead")
		super().__setattr__(key, val)


def print_world(world, header="------", overlay={}):
	print(header)
	for i, line in enumerate(world):
		print("".join(str(overlay.get((i, j), c)) for j, c in enumerate(line)))


def battle(elf_attack: int = None, *, verbose: bool = False):
	elf = lambda: (Unit("E") if elf_attack is None else Elf(elf_attack))
	world = [
		[elf() if c == "E" else Unit(c) if c == "G" else c for c in line.strip()]
		for line in raw.splitlines()
	]
	unit_counts = {c: raw.count(c) for c in "EG"}

	def around(y: int, x: int, cs: str = "."):
		for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):
			if world[y + dy][x + dx] in cs:
				yield y + dy, x + dx

	def indexed(cs: str):
		for i, line in enumerate(world):
			for j, c in enumerate(line):
				if c in cs:
					assert isinstance(c, (Elf, Unit))
					yield i, j, c

	def in_range(y: int, x: int):
		return {
			(y, x)
			for i, j, _ in indexed("EG".replace(world[y][x], ""))
			for y, x in around(i, j)
		}

	def distances(y: int, x: int):
		distance = {(y, x): 0}
		open_set = set(distance)
		while open_set:
			p0 = open_set.pop()
			d = distance[p0] + 1
			for yi, xi in around(*p0):
				p = yi, xi
				if p not in distance or d < distance[p]:
					distance[p] = d
					open_set.add(p)
		return distance

	def step(y: int, x: int):
		d = distances(y, x)
		n = min(set(in_range(y, x)) & set(d), key=lambda p: (d[p], p))
		d = distances(*n)
		s = min((d[pos], pos) for pos in around(y, x) if pos in d)[1]
		y1, x1 = s
		world[y1][x1] = world[y][x]
		world[y][x] = "."
		return s

	def units_around(y: int, x: int, unit_type: str):
		for yi, xi in around(y, x, unit_type):
			e = world[yi][xi]
			assert isinstance(e, Unit)
			yield e, yi, xi

	def attack_from(u: Unit, y: int, x: int):
		e = "EG".replace(u, "")
		try:
			t, yt, xt = min(units_around(y, x, e), key=lambda xs: xs[0].hp)
		except ValueError:
			return False
		t.hp -= u.ap
		if t.hp <= 0:
			unit_counts[t] -= 1
			world[yt][xt] = "."
		return True

	if verbose:
		print_world(world, "Initially:")

	rounds = -1
	while all(unit_counts.values()):
		for y, x, u in sorted(indexed("EG")):
			if world[y][x] != u:
				continue  # dead
			if attack_from(u, y, x):
				continue
			try:
				y, x = step(y, x)
			except ValueError:
				continue
			attack_from(u, y, x)

		rounds += 1
		if verbose:
			print_world(world, f"After {rounds} rounds:")
	return rounds * sum(c.hp for *_, c in indexed("EG"))


def find_power(lo: int, hi: int):
	while True:
		mid = (hi + lo) // 2
		try:
			res = battle(mid)
		except ValueError:
			lo = mid + 1
		else:
			if lo == hi:
				return res
			else:
				hi = mid


with open("input.txt") as f:
	raw = f.read().strip()

print("Day 15, part 1:", battle())
print("Day 15, part 2:", find_power(4, 200))
