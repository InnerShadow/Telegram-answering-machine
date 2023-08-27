import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np

from keras.layers import Dense, Embedding, LSTM, GRU
from keras.models import Sequential, load_model
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

def Get_RNN_model_answer(model, tokenizer, msg, sequences_len = 100, answer_len = 100):

    words = msg.split()

    res = ""

    if len(words) > sequences_len:
        for i in range(sequences_len):
            res += " " + words[i]
    else:
        res = msg
	
    data = tokenizer.texts_to_sequences([res])[0]

    if len(words) < sequences_len:
        while len(data) < sequences_len:
            data = [0] + data

    res = ""
			
    for i in range(answer_len):
        x = data[i : i + sequences_len]
        inp = np.expand_dims(x, axis = 0)

        pred = model.predict(inp)
        indx = pred.argmax(axis = 1)[0]
        data.append(indx)

        res += " " + tokenizer.index_word[indx]
    
    return res


def save_RNN_model(name, model):
    model.save("RNN_" + str(name[1:]) + ".h5")


def load_RNN_model(name):
    model = load_model("RNN_" + str(name[1:]) + ".h5")
    return model


def CreateRNN_word_edit(name, X, Y, tokenizer, maxWordsCount = 5000, sequences_len = 100, batch_size = 64, epochs = 50):

    X_sequences = tokenizer.texts_to_sequences(X)
    Y_sequences = tokenizer.texts_to_sequences(Y)

    qa_pairs = [(X_seq, Y_seq) for X_seq, Y_seq in zip(X_sequences, Y_sequences)]

    train_pairs, test_pairs = train_test_split(qa_pairs, test_size = 0.2)

    X_train_padded = pad_sequences([pair[0] for pair in train_pairs], maxlen=sequences_len, padding='post')
    Y_train_padded = pad_sequences([pair[1] for pair in train_pairs], maxlen=sequences_len, padding='post')

    X_test_padded = pad_sequences([pair[0] for pair in test_pairs], maxlen=sequences_len, padding='post')
    Y_test_padded = pad_sequences([pair[1] for pair in test_pairs], maxlen=sequences_len, padding='post')

    Y_train_padded_categorical = to_categorical(Y_train_padded, num_classes=maxWordsCount)
    Y_test_padded_categorical = to_categorical(Y_test_padded, num_classes=maxWordsCount)

    model = Sequential()
    model.add(Embedding(maxWordsCount, 1025, input_length = sequences_len))
    model.add(GRU(512, return_sequences = True))
    model.add(GRU(256, return_sequences = True))
    model.add(GRU(128, return_sequences = True))
    model.add(Dense(512))
    model.add(Dense(maxWordsCount, activation = 'softmax'))

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    model.summary()

    model.fit(X_train_padded, Y_train_padded_categorical, epochs = epochs, batch_size = batch_size, validation_data = (X_test_padded, Y_test_padded_categorical))

    loss, accuracy = model.evaluate(X_test_padded, Y_test_padded_categorical, verbose=0)

    save_RNN_model(name, model)

    return model

    
def CreateRNN_word_edit_2(name, X, Y, tokenizer, maxWordsCount = 5000, sequences_len = 100, batch_size = 64, epochs = 50):

    texts = ""
    for i in range(len(X)):
        texts += X[i] + " - " + Y[i] + "\n"

    data = tokenizer.texts_to_sequences([texts])
    res = np.array(data[0])

    n = res.shape[0] - sequences_len

    X = np.array([res[i:i + sequences_len] for i in range(n)])
    Y = to_categorical(res[sequences_len:], num_classes = maxWordsCount)

    model = Sequential()
    model.add(Embedding(maxWordsCount, 512, input_length = sequences_len))
    model.add(GRU(256, return_sequences = True))
    model.add(GRU(128))
    model.add(Dense(maxWordsCount, activation = 'softmax'))

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    model.summary()

    model.fit(X, Y, epochs = epochs, batch_size = batch_size)

    save_RNN_model(name, model)

    return model
