
puzzle_input = 846021
limit = puzzle_input + 10

scores = '37'
elf_a = 0
elf_b = 1

while len(scores) < limit:
	a = int(scores[elf_a])
	b = int(scores[elf_b])
	scores += str(a + b)
	elf_a = (elf_a + a + 1) % len(scores)
	elf_b = (elf_b + b + 1) % len(scores)

print("Day 14, part 1:", scores[-10:])

