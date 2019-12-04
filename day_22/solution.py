
class GeoMap:
	def __init__(self, depth, target):
		self.map = {(0, 0): 0, target: 0}
		self.depth = depth
		self.target = target

	def __getitem__(self, i):
		return self.erosion(i) % 3

	def erosion(self, i):
		if i not in self.map:
			x, y = i
			if y == 0:
				self.map[i] = x * 16807
			elif x == 0:
				self.map[i] = y * 48271
			else:
				self.map[i] = self.erosion((x - 1, y)) * self.erosion((x, y - 1))
		return (self.map[i] + self.depth) % 20183


depth = 3339
x = 10
y = 715

geo_map = GeoMap(depth, (x, y))
total = sum(geo_map[i, j] for i in range(x + 1) for j in range(y + 1))
print("Day 22, part 1: ", total)

