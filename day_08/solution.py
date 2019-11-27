
from collections import namedtuple

with open('input.txt') as f:
	license = list(map(int, f.read().split()))


Node = namedtuple('Node', ['children', 'metadata'])


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

print('Day 8, part 1:', tree_sum(tree))

