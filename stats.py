#!/usr/bin/env python3

import collections

with open("compressed.txt", "r") as file:
	counter = collections.Counter(100 * round(int(line) / 100) for line in file)

	for i, count in sorted(counter.items()):
		print(f"{i}\t{count}")
