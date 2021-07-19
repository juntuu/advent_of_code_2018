from collections import Counter


class List:
	__slots__ = ("value", "next", "prev")

	def __init__(self, v, n=None, p=None):
		self.value = v
		self.next = n or self
		self.prev = p or self

	def insert(self, val):
		new = List(val, self.next, self)
		self.next.prev = new
		self.next = new
		return new

	def remove(self):
		self.prev.next = self.next
		self.next.prev = self.prev
		return self

	def to_str(self, current=None):
		res = ""
		at = self
		while True:
			if at is current:
				res += f"({at.value:2})"
			else:
				res += f"{at.value:3} "
			at = at.next
			if at is self:
				break
		return res


def high_score(players, last_marble):
	"""
	10 players; last marble is worth 1618 points: high score is 8317
	13 players; last marble is worth 7999 points: high score is 146373
	17 players; last marble is worth 1104 points: high score is 2764
	21 players; last marble is worth 6111 points: high score is 54718
	30 players; last marble is worth 5807 points: high score is 37305
	>>> high_score(10, 1618)
	8317
	>>> high_score(13, 7999)
	146373
	>>> high_score(17, 1104)
	2764
	>>> high_score(21, 6111)
	54718
	>>> high_score(30, 5807)
	37305
	>>> high_score(9, 25)
	32
	"""
	scores = Counter()
	marbles = List(0)
	current = marbles
	for marble in range(1, last_marble + 1):
		if marble % 23 == 0:
			for _ in range(7):
				current = current.prev
			elf = marble % players
			scores[elf] += marble + current.value
			current = current.remove().next
		else:
			current = current.next.insert(marble)
	return scores.most_common(1)[0][1]


# input
"441 players; last marble is worth 71032 points"
players, last_marble = 441, 71032

print("Day 9, part 1:", high_score(players, last_marble))

print("Day 9, part 2:", high_score(players, last_marble * 100))
