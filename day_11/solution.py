
grid_serial = 7989
grid_size = 300


def power_level(x, y, serial):
	'''
	Find the fuel cell's rack ID, which is its X coordinate plus 10.
	Begin with a power level of the rack ID times the Y coordinate.
	Increase the power level by the value of the grid serial number.
	Set the power level to itself multiplied by the rack ID.
	Keep only the hundreds digit of the power level (so 12345 becomes 3; \
		numbers with no hundreds digit become 0).
	Subtract 5 from the power level.
	'''
	rack_id = x + 10
	return ((rack_id * y + serial) * rack_id) // 100 % 10 - 5


def area_power(x, y, serial):
	return sum(power_level(x+i, y+j, serial) for i in range(3) for j in range(3))


def max_power_at(serial):
	_, xy = max(
			(area_power(x, y, serial), (x, y))
			for x in range(1, grid_size - 2)
			for y in range(1, grid_size - 2))
	return xy


assert max_power_at(42) == (21, 61)

x, y = max_power_at(grid_serial)
print(f'Day 11, part 1: {x},{y}')



