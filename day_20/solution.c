
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
	N,
	E,
	S,
	W,
} Direction;

typedef struct Map {
	int x;
	int y;
	struct Map *doors[4];
	struct Map *back_doors[4];
} Map;

Map *new_entry(Map *from, Direction d) {/*{{{*/
	Map *m = from->back_doors[d];
	if (m) { return m; }
	m = calloc(1, sizeof(Map));
	if (!m) {
		perror("allocating map entry");
		exit(2);
	}
	m->x = from->x;
	m->y = from->y;
	switch (d) {
		case N: m->y -= 2; break;
		case E: m->x += 2; break;
		case S: m->y += 2; break;
		case W: m->x -= 2; break;
	}
	from->doors[d] = m;
	m->back_doors[(d + 2) % 4] = from;
	return m;
}/*}}}*/

char *build_map(char *re, Map *m) {/*{{{*/
	for (; *re; re++) {
		switch (*re) {
			case '^': break;
			case '$': return re;
			case 'N': m = new_entry(m, N); break;
			case 'E': m = new_entry(m, E); break;
			case 'S': m = new_entry(m, S); break;
			case 'W': m = new_entry(m, W); break;
			case '(': while((re = build_map(re+1, m)) && *re == '|')
					  ;
				  break;
			case '|': return re;
			case ')': return re;
		}
	}
	return re;
}/*}}}*/

void map_bounds(Map *m, int *x, int *y) {/*{{{*/
	if (!m) return;
	if (m->x < x[0]) x[0] = m->x;
	else if (m->x > x[1]) x[1] = m->x;
	if (m->y < y[0]) y[0] = m->y;
	else if (m->y > y[1]) y[1] = m->y;
	for (int i = 0; i < 4; i++)
		map_bounds(m->doors[i], x, y);
}/*}}}*/

void map_fill(Map *m, char **rows, int x_off, int y_off) {/*{{{*/
	rows[m->y - y_off][m->x - x_off] = '.';
	for (int i = 0; i < 4; i++) {
		if (!m->doors[i]) continue;
		switch (i) {
			case N: rows[m->y - y_off - 1][m->x - x_off] = '-'; break;
			case E: rows[m->y - y_off][m->x - x_off + 1] = '|'; break;
			case S: rows[m->y - y_off + 1][m->x - x_off] = '-'; break;
			case W: rows[m->y - y_off][m->x - x_off - 1] = '|'; break;
		}
		map_fill(m->doors[i], rows, x_off, y_off);
	}
}/*}}}*/

void print_map(Map *m) {/*{{{*/
	int x[2] = {m->x, m->x};
	int y[2] = {m->y, m->y};
	map_bounds(m, x, y);
	int dx = x[1] - x[0] + 3;
	int dy = y[1] - y[0] + 3;
	char **rows = malloc(dy * sizeof(char*));
	if (!rows) {
		perror("couldn't print");
		return;
	}
	for (int i = 0; i < dy; i++) {
		rows[i] = malloc((dx + 1) * sizeof(char));
		if (!rows[i]) {
			perror("couldn't print");
			while (i--) free(rows[i]);
			free(rows);
			return;
		}
		memset(rows[i], '#', dx);
		rows[i][dx] = '\0';
	}
	map_fill(m, rows, x[0] - 1, y[0] - 1);
	rows[1-y[0]][1-x[0]] = 'X';
	for (int i = 0; i < dy; i++) {
		puts(rows[i]);
		free(rows[i]);
	}
	free(rows);
}/*}}}*/

int validate_re(char *re) {/*{{{*/
#define FAIL(...) ({ fprintf(stderr, __VA_ARGS__); return 1; })
	int open = 0;
	if (*re++ != '^') FAIL("missing opening caret ^\n");
	for (; *re; re++) {
		switch (*re) {
			case '^': FAIL("^ is only allowed as the first character\n");
			case 'N':
			case 'E':
			case 'S':
			case 'W': break;
			case '(': open++; break;
			case '|': if (open <= 0) FAIL("| outside an option group\n"); break;
			case ')': if (--open < 0) FAIL("unbalanced )\n"); break;
			case '$': if (re[1]) FAIL("junk after closing $: %.4s...\n", re+1); break;
			default: FAIL("bad character: %c\n", *re);
		}
	}
	if (open) FAIL("unbalanced (");
	return 0;
#undef FAIL
}/*}}}*/

int most_doors(Map *m) {
	if (!m) return -1;
	int max = -1;
	for (int i = 0; i < 4; i++) {
		int x = most_doors(m->doors[i]);
		if (x > max) max = x;
	}
	return max + 1;
}

int further_than(Map *m, int n) {
	if (!m) return 0;
	int total = n <= 0;
	for (int i = 0; i < 4; i++) {
		total += further_than(m->doors[i], n - 1);
	}
	return total;
}

int main(int argc, char **argv) {
	int verbose = 0;
	FILE *f = stdin;
	int cap = 1024;
	char *regex = malloc(cap * sizeof(char));
	while (argc > (1 + verbose)) {/*{{{*/
		if (!verbose && strcmp(argv[1], "-v") == 0) {
			verbose = 1;
			continue;
		}
		f = fopen(argv[1 + verbose], "r");
		if (!f) {
			perror(argv[1 + verbose]);
			return 1;
		}
		break;
	}/*}}}*/
	for (int i = 0; regex; i++) {/*{{{*/
		int n = fread(regex+(i * cap), sizeof(char), cap, f);
		if (n < cap) {
			int len = i * cap + n;
			while (len && regex[len-1] != '$') len--;
			regex[len] = '\0';
			if (0 != validate_re(regex)) {
				free(regex);
				regex = NULL;
				break;
			}
			regex = realloc(regex, (len + 1) * sizeof(char));
			break;
		}
		regex = realloc(regex, (i + 2) * cap * sizeof(char));
	}/*}}}*/
	if (!regex) {/*{{{*/
		fprintf(stderr, "couldn't read regex\n");
		return 1;
	}/*}}}*/

	Map m = {};
	build_map(regex, &m);
	if (verbose) print_map(&m);
	printf("Day 20, part 1: %d\n", most_doors(&m));
	printf("Day 20, part 2: %d\n", further_than(&m, 1000));
}

