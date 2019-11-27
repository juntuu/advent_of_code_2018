
#include <stdio.h>
#include <stdlib.h>

typedef struct List {
	struct List *next;
	struct List *prev;
	int value;
} List;


List *add_after(List *node, int value, List *new) {
	new->value = value;
	new->next = node->next;
	node->next->prev = new;
	new->prev = node;
	node->next = new;
	return new;
}

void remove_node(List *node) {
	node->prev->next = node->next;
	node->next->prev = node->prev;
}

size_t high_score(int players, int last_marble) {
	size_t *scores = calloc(players, sizeof(size_t));
	if (!scores) return 0;
	List *marbles = malloc(sizeof(List) * last_marble);
	if (!marbles) {
		free(scores);
		return 0;
	}
	marbles->value = 0;
	marbles->next = marbles;
	marbles->prev = marbles;
	List *current = marbles;
	for (int m = 1; m <= last_marble; m++) {
		if (m % 23 == 0) {
			List *removed = current;
			for (int i = 0; i < 7; i++) {
				removed = removed->prev;
			}
			int elf = m % players;
			scores[elf] += m + removed->value;
			current = removed->next;
			remove_node(removed);
		} else {
			current = add_after(current->next, m, marbles + m);
		}
	}
	size_t max = 0;
	while (--players)  {
		if (scores[players] > max)
			max = scores[players];
	}
	free(marbles);
	free(scores);
	return max;
}

int main(void) {
	int players = 441;
	int last_marble = 71032;

	size_t max = high_score(players, last_marble);
	printf("Day 9, part 1: %lu\n", max);
	max = high_score(players, last_marble * 100);
	printf("Day 9, part 2: %lu\n", max);
}

