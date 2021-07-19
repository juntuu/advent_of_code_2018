from collections import namedtuple, Counter

with open("input.txt") as f:
	license = list(map(int, f.read().split()))


Node = namedtuple("Node", ["children", "metadata"])


def parse(license):
	c, m, *license = license
	children = []
	for _ in range(c):
		child, license = parse(license)
		children.append(child)
	metadata = license[:m]
	return Node(children, metadata), license[m:]


def tree_sum(node):
	return sum(node.metadata) + sum(map(tree_sum, node.children))


tree, rest = parse(license)
assert rest == []

print("Day 8, part 1:", tree_sum(tree))


def tree_value(node):
	children, meta = node
	if not children:
		return sum(meta)
	counts = Counter(meta)
	return sum(
		tree_value(children[i - 1]) * factor
		for i, factor in counts.items()
		if i - 1 in range(len(children))
	)


print("Day 8, part 2:", tree_value(tree))
