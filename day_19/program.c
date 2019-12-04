/* #ip 3 */

typedef unsigned long T;

T program(T *r) {
	T n = r[2] + 2;
	n *= n;
	n *= 19;
	n *= 11;

	T temp = r[5] + 3;
	temp *= 22;
	temp += 3;
	n += temp;

	if (r[0]) {
		temp = 27;
		temp *= 28;
		temp += 29;
		temp *= 30;
		temp *= 14;
		temp *= 32;
		n += temp;
	}

	T sum = 0;
	T i = 1;
	do {
		T j = 1;
		do {
			if ((i * j) == n) sum += i;
			j++;
		} while (j <= n);
		i++;
	} while (i <= n);

	return sum;
}

