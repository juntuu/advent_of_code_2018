
from collections import Counter

with open('input.txt') as f:
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
print('Day 2, part 2:', checksum)

