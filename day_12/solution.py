with open("input.txt") as f:
	state = f.readline().split(":", 1)[1].strip()
	rules = {}
	for line in f:
		line = line.strip()
		if not line:
			continue
		a, b = line.split(" => ")
		if b == "#":
			rules[a] = b


def step(state, rules):
	new = ".."
	while state:
		for rule, c in rules.items():
			if state.startswith(rule):
				new += c
				break
		else:
			new += "."
		state = state[1:]
	return new


def run(state, gens, *, log=False):
	zero_at = 0
	dots = "....."
	for i in range(gens):
		if state.startswith(dots * 2):
			state = state[len(dots) :]
			zero_at -= len(dots)
		else:
			state = dots + state
			zero_at += len(dots)
		if state.endswith(dots * 2):
			state = state[: -len(dots)]
		else:
			state += dots
		state = step(state, rules)
		if log:
			if i == 0:
				print("gen", "first", "plants", "total", "state", sep="\t")
			if (i + 1) % 100 == 0:
				total = sum(i - zero_at for i, c in enumerate(state) if c == "#")
				plants = state.count("#")
				first = state.find("#") - zero_at
				rep = (
					state.replace("#" * 20, "#//#").replace("#" * 10, "#/#").strip(".")
				)
				print(i + 1, first, plants, total, rep, sep="\t")
	return state, zero_at


new_state, zero_at = run(state, 20)
total = sum(i - zero_at for i, c in enumerate(new_state) if c == "#")
print("Day 12, part 1:", total)


# observing the patterns
run(state, 400, log=True)

gen = 50000000000
# from the observations
first = gen - 100
plants = 194

total = sum(range(first, first + plants))
print("Day 12, part 2:", total)
