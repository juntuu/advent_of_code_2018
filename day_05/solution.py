def polymerise(string):
	return [ord(c.upper()) * [-1, 1][c.isupper()] for c in string]


with open("input.txt") as f:
	polymer = polymerise(f.read().strip())

# polymer = polymerise('dabAcCaCBAcCcaDA')


def react(polymer):
	reacted = True
	i = 1
	while reacted:
		reacted = False
		while i < len(polymer):
			if i > 0 and polymer[i] + polymer[i - 1] == 0:
				reacted = True
				polymer.pop(i)
				polymer.pop(i - 1)
				i = i - 1
			else:
				i += 1
	return polymer


reacted = react(polymer)
print("Day 5, part 1:", len(reacted))

units = set(map(abs, reacted))
record = len(reacted)
for unit in units:
	candidate = react([e for e in reacted if abs(e) != unit])
	if len(candidate) < record:
		record = len(candidate)

print("Day 5, part 2:", record)
