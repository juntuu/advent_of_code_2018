from collections import defaultdict
from copy import deepcopy

with open("input.txt") as f:
	edges = [(field[1], field[7]) for field in map(str.split, f)]

steps = set(sum(edges, tuple()))
todo = {step: set() for step in steps}
for a, b in edges:
	todo[b].add(a)

copy = deepcopy(todo)

done = ""
while todo:
	step, *rest = sorted(s for s, pre in todo.items() if not pre)
	todo.pop(step)
	for s in todo.values():
		s.discard(step)
	done += step

print("Day 7, part 1:", done)

todo = copy
workers = 1 + 5
second = 0
free = defaultdict(set)
while todo:
	ready = free.get(second, set())
	workers += len(ready)
	for s0 in ready:
		for s1 in todo.values():
			s1.discard(s0)
	available = sorted(s for s, pre in todo.items() if not pre)
	for step in available:
		if workers < 1:
			break
		workers -= 1
		free[second + ord(step) - 4].add(step)
		todo.pop(step)
	second += 1

print("Day 7, part 2:", max(free))
