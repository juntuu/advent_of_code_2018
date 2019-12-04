/* #ip 3 */

typedef unsigned long T;

T program(T bigger) {
	T n = 905;
	if (bigger) n += 10550400;

	T sum = n;
	for (T i = 1; i < n; i++)
		if ((n % i) == 0)
			sum += i;
	return sum;
}

