#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

typedef struct {
	int x;
	int y;
	int dx;
	int dy;
} Point;

Point advance(int k, Point* ps, int n) {
	int min_x = INT_MAX;
	int min_y = INT_MAX;
	int max_x = INT_MIN;
	int max_y = INT_MIN;
	for (; n--; ps++) {
		ps->x += ps->dx * k;
		ps->y += ps->dy * k;
		if (ps->x < min_x) min_x = ps->x;
		else if (ps->x > max_x) max_x = ps->x;
		if (ps->y < min_y) min_y = ps->y;
		else if (ps->y > max_y) max_y = ps->y;
	}
	return (Point){min_x, min_y, max_x - min_x + 1, max_y - min_y + 1};
}

Point solve(Point* ps, int n, int *time) {
	Point min = advance(1, ps, n);
	Point p = advance(1, ps, n);
	while (p.dy < min.dy) {
		min = p;
		p = advance(1, ps, n);
		(*time)++;
	}
	(*time)++; /* +2 before loop -1 on the next line => +1 */
	return advance(-1, ps, n);
}

int main(int argc, char **argv) {
	FILE *f = stdin;
	if (argc > 1) {
		f = fopen(argv[1], "r");
		if (!f) {
			perror(argv[1]);
			return 1;
		}
	}
	int cap = 255;
	Point *points = malloc(cap * sizeof(Point));
	if (!points) {
		fclose(f);
		perror("allocating points");
		return 1;
	}
	int n_points = 0;
	int x, y, dx, dy;
	while (fscanf(f, "position=<%d, %d> velocity=<%d,%d>\n", &x, &y, &dx, &dy) == 4) {
		if (n_points >= cap) {
			cap *= 2;
			points = realloc(points, cap * sizeof(Point));
			if (!points) {
				fclose(f);
				perror("reallocating points");
				return 1;
			}
		}
		points[n_points++] = (Point){x, y, dx, dy};
	}
	fclose(f);

	int time = 0;
	Point bounds = solve(points, n_points, &time);

	char *buf = malloc(bounds.dx * bounds.dy * sizeof(char));
	puts("Day 10, part 1:");
	if (buf) {
		memset(buf, ' ', bounds.dx * bounds.dy);
		for (int i = 0; i < n_points; i++) {
			int offset = (points[i].y - bounds.y) * bounds.dx + points[i].x - bounds.x;
			buf[offset] = '*';
		}
		for (int i = 0; i < bounds.dy; i++) {
			write(STDOUT_FILENO, buf+i*bounds.dx, bounds.dx);
			putchar('\n');
		}
		free(buf);
	} else {
		Point p;
		for (int y = 0; y < bounds.dy; y++) {
			for (int x = 0; x < bounds.dx; x++) {
				char c = ' ';
				for (int n = 0; n < n_points; n++) {
					p = points[n];
					if (p.x == (x + bounds.x) && p.y == (y + bounds.y)) {
						c = '*';
						points[n] = points[--n_points];
						break;
					}
				}
				putchar(c);
			}
			putchar('\n');
		}
	}
	free(points);
	printf("Day 10, part 2: %d\n", time);
}

