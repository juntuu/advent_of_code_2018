from collections import Counter


def high_score(players, last_marble):
	'''
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
	'''
	scores = Counter()
	marbles = [0]
	current = 0
	for marble in range(1, last_marble + 1):
		if marble % 23 == 0:
			remove = (current + len(marbles) - 7) % len(marbles)
			removed = marbles.pop(remove)
			current = remove
			elf = marble % players
			scores[elf] += marble + removed
		else:
			current = (current + 1) % len(marbles) + 1
			marbles.insert(current, marble)
	return scores.most_common(1)[0][1]


# input
'441 players; last marble is worth 71032 points'
players, last_marble = 441, 71032

print('Day 9, part 1:', high_score(players, last_marble))

