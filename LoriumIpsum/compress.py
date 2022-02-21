#!/usr/bin/env python3

import re

with open("text.txt", "r") as inp, open("text.bin", "wb") as outp:
	def write_compact(seq):
		size = max(seq).bit_length()
		bits = 0

		for i in reversed(seq):
			bits = bits << size | i

		outp.write(bits.to_bytes((bits.bit_length() + 8 - 1) // 8, "big"))

	word_map = {}
	words = []
	tokens = []

	for match in re.finditer(r"([a-zA-Z]+)|([,.?])", inp.read()):
		token = match[0].lower()

		if match.lastindex == 1:
			if token not in word_map:
				words.append(token)

			tokens.append(word_map.setdefault(token, len(word_map) + 3))
		else:
			tokens.append(",.?".index(token))

	write_compact([ord(char) - ord("a") for char in chr(ord("z") + 1).join(words)])
	write_compact(tokens)
