#include <stdio.h>
#include <string.h>

typedef struct {
	int data[4];
} Registers;

#define RESOLVED_OPCODES
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

typedef struct {/*{{{*/
	Opcode opcode;
	int A;
	int B;
	int C;
} Instruction;/*}}}*/

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

int test(Instruction i, Registers before, Registers after) {/*{{{*/
	if (excecute(i, &before)) return 0;
	return 0 == memcmp(&before, &after, sizeof(Registers));
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

	int limit = 3;
	int matches = 0;
	int rev_mappings[N_OPCODES] = {};
	Instruction input;
	Registers before;
	Registers after;
	int vs[4];
	int x = 0;
	while (1) {
		x = fscanf(f, "Before: [%d,%d,%d,%d]\n", vs, vs+1, vs+2, vs+3);
		if (x != 4) break;
		memcpy(before.data, vs, sizeof(vs));
		x = fscanf(f, "%d %d %d %d\n", vs, vs+1, vs+2, vs+3);
		if (x != 4) goto bad_input;
		int original = vs[0];
		input.A = vs[1];
		input.B = vs[2];
		input.C = vs[3];
		x = fscanf(f, "After: [%d,%d,%d,%d]\n\n", vs, vs+1, vs+2, vs+3);
		if (x != 4) { bad_input:/*{{{*/
			puts("bad input");
			fclose(f);
			return 1;
		}/*}}}*/
		memcpy(after.data, vs, sizeof(vs));
		int match = 0;
		for (int i = 0; i < N_OPCODES; i++) {
			input.opcode = i;
			if (test(input, before, after)) {
				rev_mappings[i] |= 1 << original;
				match++;
			}
		}
		if (match >= limit) matches++;
	}
	printf("Day 16, part 1: %d\n", matches);

#ifdef RESOLVED_OPCODES
#define RESOLVE(x) x
#else
#define RESOLVE(x) true_mapping[x]
	int true_mapping[N_OPCODES];
	for (int known = 0; known < N_OPCODES;) {
		for (int i = 0; i < N_OPCODES; i++) {
			if (!rev_mappings[i]) continue;
			int count = 0;
			int op = 0;
			for (int j = 0; j < N_OPCODES; j++) {
				if (rev_mappings[i] & (1 << j)) {
					op = j;
					if (count++) break;
				}
			}
			if (count == 1) {
				true_mapping[op] = i;
				known++;
				for (int i = 0; i < N_OPCODES; i++)
					rev_mappings[i] &= ~(1 << op);
			}
		}
	}

	for (int i = 0; i < N_OPCODES; i++)
		rev_mappings[true_mapping[i]] = i;
	for (int i = 0; i < N_OPCODES; i++)
		printf("%2d -> %2d\n", i, rev_mappings[i]);
#endif

	Registers reg = {};
	while (4 == fscanf(f, "%d %d %d %d\n", vs, vs+1, vs+2, vs+3)) {
		Instruction i = {RESOLVE(vs[0]), vs[1], vs[2], vs[3]};
		excecute(i, &reg);
	}
	fclose(f);
	printf("Day 16, part 2: %d\n", reg.data[0]);
}/*}}}*/

