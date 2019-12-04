/* #ip 3 */

typedef unsigned long T;

T program(T *r) {
ip_0:
	goto ip_17;
ip_1:
	r[1] = 1;
ip_2:
	r[4] = 1;
ip_3:
	r[5] = r[1] * r[4];
ip_4:
	r[5] = r[5] == r[2];
ip_5:
	if (r[5]) goto ip_7;
ip_6:
	goto ip_8;
ip_7:
	r[0] = r[1] + r[0];
ip_8:
	r[4] = r[4] + 1;
ip_9:
	r[5] = r[4] > r[2];
ip_10:
	if (r[5]) goto ip_12;
ip_11:
	goto ip_3;
ip_12:
	r[1] = r[1] + 1;
ip_13:
	r[5] = r[1] > r[2];
ip_14:
	if (r[5]) goto ip_16;
ip_15:
	goto ip_2;
ip_16:
	return r[0];
ip_17:
	r[2] = r[2] + 2;
ip_18:
	r[2] = r[2] * r[2];
ip_19:
	r[2] = 19 * r[2];
ip_20:
	r[2] = r[2] * 11;
ip_21:
	r[5] = r[5] + 3;
ip_22:
	r[5] = r[5] * 22;
ip_23:
	r[5] = r[5] + 3;
ip_24:
	r[2] = r[2] + r[5];
ip_25:
	if (r[0]) goto ip_27;
ip_26:
	goto ip_1;
ip_27:
	r[5] = 27;
ip_28:
	r[5] = r[5] * 28;
ip_29:
	r[5] = 29 + r[5];
ip_30:
	r[5] = 30 * r[5];
ip_31:
	r[5] = r[5] * 14;
ip_32:
	r[5] = r[5] * 32;
ip_33:
	r[2] = r[2] + r[5];
ip_34:
	r[0] = 0;
ip_35:
	goto ip_1;
}

