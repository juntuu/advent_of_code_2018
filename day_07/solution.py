
with open('input.txt') as f:
	edges = [(field[1], field[7]) for field in map(str.split, f)]

steps = set(sum(edges, tuple()))
todo = {step: set() for step in steps}
for a, b in edges:
	todo[b].add(a)

done = ''
while todo:
	step, *rest = sorted(s for s, pre in todo.items() if not pre)
	todo.pop(step)
	for s in todo.values():
		s.discard(step)
	done += step

print('Day 7, part 1:', done)

