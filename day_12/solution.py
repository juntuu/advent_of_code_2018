
with open('input.txt') as f:
	state = f.readline().split(':', 1)[1].strip()
	rules = {}
	for line in f:
		line = line.strip()
		if not line:
			continue
		a, b = line.split(' => ')
		if b == '#':
			rules[a] = b


def step(state, rules):
	new = '..'
	while state:
		for rule, c in rules.items():
			if state.startswith(rule):
				new += c
				break
		else:
			new += '.'
		state = state[1:]
	return new


zero_at = 0
dots = '.....'
for i in range(20):
	if state.startswith(dots * 2):
		state = state[len(dots):]
		zero_at -= len(dots)
	else:
		state = dots + state
		zero_at += len(dots)
	if state.endswith(dots * 2):
		state = state[:-len(dots)]
	else:
		state += dots
	state = step(state, rules)

total = sum(i - zero_at for i, c in enumerate(state) if c == '#')
print('Day 12, part 1:', total)

