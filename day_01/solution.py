
with open('input.txt') as f:
	frequencies = [int(line) for line in f]

print('Day 1, part 1:', sum(frequencies))
