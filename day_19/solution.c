#include <stdio.h>
#include <stdlib.h>

typedef struct {
	int data[6];
} Registers;

typedef enum {/*{{{*/
	addr = 12,
	addi = 14,
	mulr = 7,
	muli = 3,
	banr = 10,
	bani = 15,
	borr = 5,
	bori = 6,
	setr = 0,
	seti = 9,
	gtir = 13,
	gtri = 2,
	gtrr = 8,
	eqir = 4,
	eqri = 11,
	eqrr = 1,
	N_OPCODES = 16,
} Opcode;/*}}}*/

Opcode parse_opcode(char code[4]) { /*{{{ hideous switch mess */
	switch (code[0]) {
		case 'a':
			switch (code[3]) {
				case 'r': return addr;
				case 'i': return addi;
			}
		case 'm':
			switch (code[3]) {
				case 'r': return mulr;
				case 'i': return muli;
			}
		case 'b':
			switch (code[3]) {
				case 'r': return code[1] == 'o' ? borr : banr;
				case 'i': return code[1] == 'o' ? bori : bani;
			}
		case 's':
			switch (code[3]) {
				case 'r': return setr;
				case 'i': return seti;
			}
		case 'g':
			switch (code[3]) {
				case 'r': return code[2] == 'i' ? gtir : gtrr;
				case 'i': return gtri;
			}
		case 'e':
			switch (code[3]) {
				case 'r': return code[2] == 'i' ? eqir : eqrr;
				case 'i': return eqri;
			}
	}
	return -1;
}/*}}}*/

typedef struct {/*{{{*/
	Opcode opcode;
	int A;
	int B;
	int C;
} Instruction;/*}}}*/

typedef struct {/*{{{*/
	Instruction *i;
	int n;
	int bound_register;
} Program;/*}}}*/

int excecute(Instruction i, Registers *r) {/*{{{*/
	int *reg = r->data;
	switch (i.opcode) {/*{{{*/
		/* Addition:{{{
		 * addr stores into r C the result of adding r A and r B.
		 * addi stores into r C the result of adding r A and i B.
		 */
		case addr: reg[i.C] = reg[i.A] + reg[i.B];
			   break;
		case addi: reg[i.C] = reg[i.A] + i.B;
			   break;/*}}}*/
			   /* Multiplication:{{{
			    * mulr stores into r C the result of multiplying r A and r B.
			    * muli stores into r C the result of multiplying r A and i B.
			    */
		case mulr: reg[i.C] = reg[i.A] * reg[i.B];
			   break;
		case muli: reg[i.C] = reg[i.A] * i.B;
			   break;/*}}}*/
			   /* Bitwise AND:{{{
			    * banr stores into r C the result of the bitwise AND of r A and r B.
			    * bani stores into r C the result of the bitwise AND of r A and i B.
			    */
		case banr: reg[i.C] = reg[i.A] & reg[i.B];
			   break;
		case bani: reg[i.C] = reg[i.A] & i.B;
			   break;/*}}}*/
			   /* Bitwise OR:{{{
			    * borr stores into r C the result of the bitwise OR of r A and r B.
			    * bori stores into r C the result of the bitwise OR of r A and i B.
			    */
		case borr: reg[i.C] = reg[i.A] | reg[i.B];
			   break;
		case bori: reg[i.C] = reg[i.A] | i.B;
			   break;/*}}}*/
			   /* Assignment:{{{
			    * setr copies the contents of r A into r C. (Input B is ignored.)
			    * seti stores i A into r C. (Input B is ignored.)
			    */
		case setr: reg[i.C] = reg[i.A];
			   break;
		case seti: reg[i.C] = i.A;
			   break;/*}}}*/
			   /* Greater-than testing:{{{
			    * gtir sets r C to 1 if i A is greater than r B. Otherwise, r C is set to 0.
			    * gtri sets r C to 1 if r A is greater than i B. Otherwise, r C is set to 0.
			    * gtrr sets r C to 1 if r A is greater than r B. Otherwise, r C is set to 0.
			    */
		case gtir: reg[i.C] = i.A > reg[i.B];
			   break;
		case gtri: reg[i.C] = reg[i.A] > i.B;
			   break;
		case gtrr: reg[i.C] = reg[i.A] > reg[i.B];
			   break;/*}}}*/
			   /* Equality testing:{{{
			    * eqir sets r C to 1 if i A is equal to r B. Otherwise, r C is set to 0.
			    * eqri sets r C to 1 if r A is equal to i B. Otherwise, r C is set to 0.
			    * eqrr sets r C to 1 if r A is equal to r B. Otherwise, r C is set to 0.
			    */
		case eqir: reg[i.C] = (i.A == reg[i.B]);
			   break;
		case eqri: reg[i.C] = (reg[i.A] == i.B);
			   break;
		case eqrr: reg[i.C] = (reg[i.A] == reg[i.B]);
			   break;/*}}}*/
		default: printf("unknown opcode: %d\n", i.opcode); return 1;
	}/*}}}*/
	return 0;
}/*}}}*/

unsigned long run(Program p, Registers *r) {/*{{{*/
	unsigned long cycles = 0;
	int ip_;
	int *ip = &ip_;
	if (p.bound_register >= 0) {
		ip = &r->data[p.bound_register];
	}
	*ip = 0;
	while (0 <= *ip && *ip < p.n) {
		excecute(p.i[*ip], r);
		(*ip)++;
		cycles++;
	}
	if (cycles > 0) (*ip)--;
	return cycles;
}/*}}}*/

Program read_program(FILE *f) {/*{{{*/
	char opcode[4];
	int a, b, c;
	Program p = { .n = 0 };
	int cap = 64;
	p.i = malloc(cap * sizeof(Instruction));
	if (!p.i) {
		perror("allocating instructions");
		return p;
	}
	while (1) { /*{{{ parse program */
		int x = fscanf(f, "%4c%d%d%d\n", opcode, &a, &b, &c);
		if (x == 2 && opcode[0] == '#') {
			p.bound_register = a;
			continue;
		}
		if (x != 4) {/*{{{*/
			cap = p.n;
			p.i = realloc(p.i, cap * sizeof(Instruction));
			if (!p.i) {
				perror("reallocating instructions");
				p.n = 0;
				return p;
			}
			break;
		}/*}}}*/
		if (p.n >= cap) {/*{{{*/
			cap *= 2;
			p.i = realloc(p.i, cap * sizeof(Instruction));
			if (!p.i) {
				perror("reallocating instructions");
				p.n = 0;
				return p;
			}
		}/*}}}*/

		int op = parse_opcode(opcode);
		if (op < 0) {
			printf("unknown opcode: %.4s\n", opcode);
			free(p.i);
			p.i = NULL;
			p.n = 0;
			return p;
		}
		p.i[p.n++] = (Instruction) { op, a, b, c };
	}/*}}}*/
	return p;
}/*}}}*/

int main(int argc, char **argv) {/*{{{*/
	FILE *f = stdin;/*{{{*/
	if (argc > 1) {
		f = fopen(argv[1], "r");
		if (!f) {
			perror(argv[1]);
			return 1;
		}
	}/*}}}*/

	Program p = read_program(f);
	fclose(f);

	if (!p.i) {
		puts("couldn't read the program");
		return 1;
	}

	Registers r = {};
	run(p, &r);
	printf("Day 19, part 1: %d\n", r.data[0]);

	free(p.i);
}/*}}}*/

