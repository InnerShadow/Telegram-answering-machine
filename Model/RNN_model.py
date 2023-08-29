import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np

from keras.layers import Dense, Embedding, LSTM, GRU
from keras.models import Sequential, load_model
from keras.utils import to_categorical

from Data_manupulation.Words_level import word_level_prerpocessing

def save_RNN_model(name, model):
    model.save("RNN_" + str(name[1:]) + ".h5")


def load_RNN_model(name):
    model = load_model("RNN_" + str(name[1:]) + ".h5")
    return model


def sequence_RNN_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount):
    for i in range(epochs):
        print("epoch " + str(i) + " from " + str(epochs))
        index = 0
        for k in range(int(len(X) / batch_size)):
            texts = ""
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

            index += batch_size

            model.fit(X_train, Y_train, batch_size = batch_size)

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


def RNN_word_continue(name, X, Y, tokenizer, maxWordsCount = 5000, sequences_len = 100, batch_size = 64, epochs = 50):

    model = Sequential()
    model.add(Embedding(maxWordsCount, 1024, input_length = sequences_len))
    model.add(LSTM(512, return_sequences = True))
    model.add(GRU(256, return_sequences = True))
    model.add(GRU(128, return_sequences = True))
    model.add(GRU(64))
    model.add(Dense(maxWordsCount, activation = 'softmax'))

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    model.summary()

    model = sequence_RNN_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount)
    #model = random_sequence_RNN_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount)
    #model = random_RNN_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount)

    save_RNN_model(name, model)

    return model

    
def RNN_word_edit_QA_model(name, X, Y, tokenizer, maxWordsCount = 5000, sequences_len = 100, batch_size = 64, epochs = 50):

    data = word_level_prerpocessing(X, Y, tokenizer, sequences_len)

    model = Sequential()
    model.add(Embedding(maxWordsCount, 1024, input_length = sequences_len))
    model.add(LSTM(512, return_sequences = True))
    model.add(GRU(256, return_sequences = True))
    model.add(GRU(128))
    model.add(Dense(maxWordsCount, activation = 'softmax'))

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    model.summary()

    #model.fit(X, Y, epochs = epochs, batch_size = batch_size)

    for i in range(epochs):
        for j in range(batch_size):
            print("Batch: " + str(j + 1) + " from " + str(batch_size) + ", epochs: " + str(i + 1) + " from " + str(epochs))
            indx = np.random.randint(0, len(data) - 1)
            res = np.array(data[indx])

            n = res.shape[0] - sequences_len

            X = np.array([res[i:i + sequences_len] for i in range(n)])
            Y = to_categorical(res[sequences_len:], num_classes = maxWordsCount)

            model.fit(X, Y, batch_size)


    save_RNN_model(name, model)

    return model
