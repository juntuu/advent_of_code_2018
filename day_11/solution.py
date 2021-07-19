grid_serial = 7989
grid_size = 300


def power_level(x, y, serial):
	"""
	Find the fuel cell's rack ID, which is its X coordinate plus 10.
	Begin with a power level of the rack ID times the Y coordinate.
	Increase the power level by the value of the grid serial number.
	Set the power level to itself multiplied by the rack ID.
	Keep only the hundreds digit of the power level (so 12345 becomes 3; \
		numbers with no hundreds digit become 0).
	Subtract 5 from the power level.
	"""
	rack_id = x + 10
	return ((rack_id * y + serial) * rack_id) // 100 % 10 - 5


def area_power(x, y, z, serial, cache):
	power = cache.get((x, y, z))
	if power is not None:
		return power

	if z < 4:
		power = sum(
			power_level(x + i, y + j, serial) for i in range(z) for j in range(z)
		)
		cache[(x, y, z)] = power

	k, i = divmod(z, 2)
	if i == 0:
		power = area_power(x, y, k, serial, cache)
		power += area_power(x + k, y, k, serial, cache)
		power += area_power(x, y + k, k, serial, cache)
		power += area_power(x + k, y + k, k, serial, cache)
	else:
		power = area_power(x, y, k + i, serial, cache)
		power += area_power(x + k + i, y, k, serial, cache)
		power += area_power(x, y + k + i, k, serial, cache)
		power += area_power(x + k, y + k, k + i, serial, cache)
		power -= area_power(x + k, y + k, i, serial, cache)

	cache[(x, y, z)] = power
	return power


def max_power_at(serial, sub_range=(3,)):
	cache = {}
	powers = []

	for z in sub_range:
		powers.append(
			max(
				(area_power(x, y, z, serial, cache), (x, y, z))
				for x in range(1, grid_size - (z - 2))
				for y in range(1, grid_size - (z - 2))
			)
		)
	_, xyz = max(powers)
	return xyz


assert max_power_at(42)[:2] == (21, 61)

x, y, _ = max_power_at(grid_serial)
print(f"Day 11, part 1: {x},{y}")

assert max_power_at(18, range(1, grid_size + 1)) == (90, 269, 16)
assert max_power_at(42, range(1, grid_size + 1)) == (232, 251, 12)

x, y, z = max_power_at(grid_serial, range(1, grid_size + 1))
print(f"Day 11, part 2: {x},{y},{z}")
