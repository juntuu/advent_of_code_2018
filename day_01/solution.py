from itertools import cycle

with open("input.txt") as f:
	frequencies = [int(line) for line in f]

print("Day 1, part 1:", sum(frequencies))

repeated_frequensies = cycle(frequencies)

total = 0
seen = {total}
for change in repeated_frequensies:
	total += change
	if total in seen:
		print("Day 1, part 2:", total)
		break
	seen.add(total)
