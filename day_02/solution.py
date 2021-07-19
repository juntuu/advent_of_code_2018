from collections import Counter

with open("input.txt") as f:
	ids = [line.strip() for line in f]


def counts(line):
	counter = Counter(line)
	values = set(counter.values())
	return (2 in values, 3 in values)


twos = 0
threes = 0
for two, three in map(counts, ids):
	twos += two
	threes += three

checksum = twos * threes
print("Day 2, part 2:", checksum)


def similar(needle, haystack, differences=1):
	for straw in haystack:
		diff = sum(a != b for a, b in zip(needle, straw))
		if diff == differences:
			return straw


for i, line in enumerate(ids):
	other = similar(line, ids[i:])
	if other:
		letters = "".join(c for i, c in enumerate(line) if other[i] == c)
		print("Day 2, part 2:", letters)
		break
