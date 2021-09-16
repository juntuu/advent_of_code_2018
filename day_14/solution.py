def run(elf_a, elf_b, scores, *, limit=None, rounds=None):
	assert [limit, rounds].count(None) == 1
	each = range(rounds) if limit is None else iter(lambda: len(scores) < limit, False)
	for _ in each:
		a = int(scores[elf_a])
		b = int(scores[elf_b])
		scores += str(a + b)
		elf_a = (elf_a + a + 1) % len(scores)
		elf_b = (elf_b + b + 1) % len(scores)
	return elf_a, elf_b, scores


puzzle_input = 846021

elf_a, elf_b, scores = run(0, 1, "37", limit=puzzle_input + 10)
print("Day 14, part 1:", scores[-10:])

looking_for = str(puzzle_input)
pos = scores.find(looking_for)
while pos < 0:
	i = len(scores) - len(looking_for)
	elf_a, elf_b, scores = run(elf_a, elf_b, scores, rounds=puzzle_input)
	pos = scores.find(looking_for, i)

print("Day 14, part 2:", pos)
