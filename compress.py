#!/usr/bin/env python3

import math

with open("compressed.txt", "r") as inp, open("compressed.bin", "wb") as outp:
	indices = list(map(int, inp))
	size = math.ceil(math.log2(max(indices)))
	bits = 0

	for i in reversed(indices):
		bits = bits << size | i

	outp.write(bits.to_bytes((bits.bit_length() + 8 - 1) // 8, "big"))
