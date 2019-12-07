

class Unit(str):
	hp = 200
	ap = 3


class Elf(str):
	hp = 200

	def __new__(cls, ap):
		e = super().__new__(cls, 'E')
		e.ap = ap
		return e

	def __setattr__(self, key, val):
		if key == 'hp':
			assert val > 0
		super().__setattr__(key, val)


def print_world(world, header='------', overlay={}):
	print(header)
	for i, line in enumerate(world):
		s = ''.join(str(overlay.get((i, j), c)) for j, c in enumerate(line))
		print(s)


def battle(world, *, quiet=False):
	def around(y, x):
		for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
			yield y + dy, x + dx, world[y + dy][x + dx]

	def indexed():
		for i, line in enumerate(world):
			for j, c in enumerate(line):
				yield i, j, c

	def get_units():
		units = [(i, j, c) for i, j, c in indexed() if c in 'EG']
		units.sort()
		return units

	def in_range(y, x):
		e = 'EG'.replace(world[y][x], '')
		s = set()
		for i, j, c in indexed():
			if c == e:
				for y, x, c in around(i, j):
					if c == '.':
						s.add((y, x))
		return s

	def distances(y, x):
		start = y, x
		open_set = {start}
		distances = {start: 0}
		while open_set:
			p0 = open_set.pop()
			for yi, xi, c in around(*p0):
				if c != '.':
					continue
				d = distances[p0] + 1
				p = yi, xi
				if p not in distances or d < distances[p]:
					distances[p] = d
					open_set.add(p)
		return distances

	def nearest(y, x):
		r = in_range(y, x)
		d = distances(y, x)
		return min(set(r) & set(d), key=lambda p: (d[p], p))

	def step(y, x):
		n = nearest(y, x)
		d = distances(*n)
		opt = ((d[y, x], y, x) for y, x, _ in around(y, x) if (y, x) in d)
		s = min(opt)[1:]
		y1, x1 = s
		world[y1][x1] = world[y][x]
		world[y][x] = '.'
		return s

	def attack_from(y, x):
		e = 'EG'.replace(world[y][x], '')
		ts = ((c.hp, yi, xi) for yi, xi, c in around(y, x) if c == e)
		_, yt, xt = min(ts)
		t = world[yt][xt]
		t.hp -= world[y][x].ap
		if t.hp <= 0:
			world[yt][xt] = '.'

	def take_turn(y, x):
		try:
			attack_from(y, x)
		except (TypeError, ValueError):
			try:
				attack_from(*step(y, x))
			except (TypeError, ValueError):
				pass

	if not quiet:
		print_world(world, 'Initially:')
	units = get_units()
	rounds = 0
	while True:
		for y, x, u in units:
			if world[y][x] != u:
				continue  # dead
			take_turn(y, x)
		units = get_units()
		if any(u == 'E' for *_, u in units) and any(u == 'G' for *_, u in units):
			rounds += 1
			if not quiet:
				print_world(world, f'After {rounds} rounds:')
		else:
			break
	return rounds * sum(c.hp for *_, c in indexed() if c in 'EG')


with open('input.txt') as f:
	raw = f.read().strip()

world = [[Unit(c) if c in 'EG' else c for c in line.strip()] for line in raw.splitlines()]
print('Day 15, part 1:', battle(world, quiet=True))


def create_world(raw, elf_attack):
	world = []
	for line in raw.splitlines():
		world.append([])
		for c in line.strip():
			if c == 'E':
				world[-1].append(Elf(elf_attack))
			elif c == 'G':
				world[-1].append(Unit(c))
			else:
				world[-1].append(c)
	return world


def try_power(i):
	world = create_world(raw, i)
	try:
		return battle(world, quiet=True)
	except AssertionError:
		return None


lo, hi = 4, 200
while True:
	mid = (hi + lo) // 2
	res = try_power(mid)
	if res is None:
		lo = mid + 1
	elif lo == hi:
		break
	else:
		hi = mid

print('Day 15, part 2:', res)

