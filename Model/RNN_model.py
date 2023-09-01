import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np

from keras.layers import Dense, Embedding, LSTM, GRU
from keras.models import Sequential, load_model
from keras.utils import to_categorical

from Data_manupulation.Words_level import word_level_prerpocessing

from keras.preprocessing.sequence import pad_sequences


def save_RNN_model(name, model):
    model.save("Data/RNN_" + str(name[1:]) + ".h5")


def load_RNN_model(name):
    model = load_model("Data/RNN_" + str(name[1:]) + ".h5")
    return model


def QA_model_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount):

    for i in range(epochs):
        index = 0
        for j in range(int(len(X) / batch_size)):
            Q = []
            A = []
            for k in range(index, index + batch_size):

                if k >= len(X):
                    break

                Q.append(X[k])
                A.append(Y[k])

            data_X = pad_sequences(tokenizer.texts_to_sequences(Q), maxlen = sequences_len)
            data_Y = pad_sequences(tokenizer.texts_to_sequences(A), maxlen = sequences_len, padding = 'post')

            Y_categorical = to_categorical(data_Y, num_classes = maxWordsCount)

            index += batch_size

            model.fit(data_X, Y_categorical)

    return model


def full_sequence_RNN_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount):
    texts = ""
    for j in range(len(X)):
        texts += X[j] + " - " + Y[j] + " \n "

    data = tokenizer.texts_to_sequences([texts])
    res = np.array(data[0])

    n = res.shape[0] - sequences_len

    X_train = np.array([res[k:k + sequences_len] for k in range(n)])
    Y_train = to_categorical(res[sequences_len:], num_classes = maxWordsCount)

    model.fit(X_train, Y_train, batch_size = batch_size, epochs = epochs)

    return model


def sequence_RNN_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount):
    for i in range(epochs):
        print("epoch " + str(i) + " from " + str(epochs))
        index = 0
        for k in range(int(len(X) / batch_size)):
            texts = ""
            rand_shift = np.random.randint(int(-0.1 * batch_size), 0)
            for j in range(index + rand_shift, index + batch_size):
                if j >= len(X):
                    break

                if j < 0:
                    continue
                
                texts += X[j] + " - " + Y[j] + " \n "

            data = tokenizer.texts_to_sequences([texts])
            res = np.array(data[0])

            n = res.shape[0] - sequences_len

            if n <= 0:
                continue

            X_train = np.array([res[k:k + sequences_len] for k in range(n)])
            Y_train = to_categorical(res[sequences_len:], num_classes = maxWordsCount)

            index += batch_size

            model.fit(X_train, Y_train, batch_size = batch_size, epochs = 5)

    return model


def random_sequence_RNN_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount):
    for i in range(epochs):
        print("epoch " + str(i) + " from " + str(epochs))
        texts = ""
        index = np.random.randint(0, len(X) - 1)
        for j in range(index, index + batch_size):
            if j >= len(X):
                break
            
            texts += X[index] + " - " + Y[index] + " \n "

        
        data = tokenizer.texts_to_sequences([texts])
        res = np.array(data[0])

        n = res.shape[0] - sequences_len

        if n <= 0:
            continue

        X_train = np.array([res[k:k + sequences_len] for k in range(n)])
        Y_train = to_categorical(res[sequences_len:], num_classes = maxWordsCount)

        model.fit(X_train, Y_train, batch_size = batch_size)

    return model


def random_RNN_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount):
    for i in range(epochs):
        print("epoch " + str(i) + " from " + str(epochs))
        texts = ""
        
        for j in range(batch_size):
            index = np.random.randint(0, len(X) - 1)
            
            texts += X[index] + " - " + Y[index] + " \n "
        
        data = tokenizer.texts_to_sequences([texts])
        res = np.array(data[0])

        n = res.shape[0] - sequences_len

        if n <= 0:
                continue

        X_train = np.array([res[k:k + sequences_len] for k in range(n)])
        Y_train = to_categorical(res[sequences_len:], num_classes = maxWordsCount)

        model.fit(X_train, Y_train, batch_size = batch_size)

    return model


def Get_RNN_word_continue(maxWordsCount = 5000, sequences_len = 100):

    model = Sequential()
    model.add(Embedding(maxWordsCount, 256, input_length = sequences_len))
    model.add(LSTM(128, return_sequences = True))
    model.add(GRU(64))
    model.add(Dense(maxWordsCount, activation = 'softmax'))

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    model.summary()

    return model


def Get_RNN_QA(maxWordsCount = 5000, sequences_len = 100):

    model = Sequential()
    model.add(Embedding(maxWordsCount, 256, input_length = sequences_len))
    model.add(LSTM(128, return_sequences = True))
    model.add(GRU(64, return_sequences = True))
    model.add(Dense(maxWordsCount, activation = 'softmax'))

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    model.summary()

    return model

