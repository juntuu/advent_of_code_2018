with open("input.txt") as f:
	points = [tuple(map(int, line.split(","))) for line in f]


def manhattan(a, b):
	return sum(abs(i - j) for (i, j) in zip(a, b))


def join(p0, points, distance):
	group = {p0}
	added = {p0}
	checked = set()
	while added:
		p0 = added.pop()
		for p in points:
			if manhattan(p0, p) <= distance:
				added.add(p)
		checked.add(p0)
		added -= checked
		group.update(added)
	return group


def constellations(points, distance=3):
	groups = []
	not_grouped = set(points)
	while not_grouped:
		p = not_grouped.pop()
		group = join(p, points, distance)
		not_grouped -= group
		groups.append(group)
	return groups


print(len(constellations(points)))
