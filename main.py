#!/usr/bin/env python3

from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Embedding, LSTM
from keras.models import Sequential, load_model
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from keras.utils import to_categorical
import numpy
import os
import re
import sys

with open("republic_clean.txt", "r") as file:
	text = re.sub(r"^BOOK .+$", "", file.read(), flags=re.M)
	words = text_to_word_sequence(text)

	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(words)

	context_len = 50
	vocab_size = len(tokenizer.word_index) + 1
	sequences = [seq[0] for seq in tokenizer.texts_to_sequences(words)]

	# Fast replacement for keras.preprocessing.sequence.pad_sequences(sequences)
	x = numpy.array([[0] * (context_len - i) + sequences[max(i - context_len, 0):i]
	                 for i in range(len(sequences))])

	# Regex match for the newest model file
	match = next(filter(None, map(
		re.compile(r"^model-([0-9]{2})-[0-9]\.[0-9]{4}\.h5$").match,
		sorted(filter(os.path.isfile, os.listdir()), reverse=True))
	), None)

	model = Sequential([
		Embedding(vocab_size, 50, mask_zero=True, input_length=context_len),
		LSTM(100, return_sequences=True),
		LSTM(100),
		Dense(100, activation="relu"),
		Dense(vocab_size, activation="softmax")
	]) if match is None else load_model(match.group(0))

	if len(sys.argv) > 1 and sys.argv[1] in ("-t", "--test"):
		with open("compressed.txt", "w") as file:
			for i, context in enumerate(x):
				output = model.predict(numpy.array([context]))[0]
				file.write(f"{sum(prob > output[sequences[i]] for prob in output)}\n")
	else:
		model.summary()
		print()

		model.compile(optimizer="adam",
		              loss="categorical_crossentropy",
		              metrics=["accuracy"])

		y = to_categorical(sequences, num_classes=vocab_size)

		model.fit(x, y, batch_size=64, epochs=10, verbose=1, callbacks=[
			ModelCheckpoint("model-{epoch:02d}-{loss:.4f}.h5")
		], initial_epoch=0 if match is None else int(match.group(1)))
