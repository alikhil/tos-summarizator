import numpy
import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


# preprocessing
filename = sys.argv[1] if len(sys.argv) >= 2 else "example.txt"
epochs = int(sys.argv[2]) if len(sys.argv) == 3 else 20

raw_text = open(filename).read().lower()

chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))

n_chars = len(raw_text)
n_vocab = len(chars)
print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)

seq_lenght = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_lenght, 1):
    seq_in = raw_text[i:i + seq_lenght]
    seq_out = raw_text[i + seq_lenght]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("Total patters: ", n_patterns)

# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_lenght, 1))
# normalize
X = X / float(n_vocab)
# one hot encoder the output variable
y = np_utils.to_categorical(dataY)


# define the LSTM model

model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# model = Sequential()
# model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
# model.add(Dropout(0.2))
# model.add(Dense(y.shape[1], activation='softmax'))
# model.compile(loss="categorical_crossentropy", optimizer="adam")

# define the checkpoint
filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.fit(X, y, epochs=epochs, batch_size=64, callbacks=callbacks_list)