import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np

from keras.layers import Dense, Embedding, LSTM, GRU
from keras.models import Sequential, load_model
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

def Get_RNN_model_answer(model, tokenizer, msg, sequences_len = 100):

    new_questions = msg
    new_question_sequences = tokenizer.texts_to_sequences(new_questions)
    new_question_padded = pad_sequences(new_question_sequences, maxlen = sequences_len, padding = 'post')

    predicted_answers = model.predict(new_question_padded)
    answer = ""

    for i in range(sequences_len):
        idx = np.argmax(predicted_answers[0][i])
        if(idx != 0):
            answer += " " + tokenizer.index_word[idx]

    return answer


def save_RNN_model(name, model):
    model.save("RNN_" + str(name[1:]) + ".h5")


def load_RNN_model(name):
    model = load_model("RNN_" + str(name[1:]) + ".h5")
    return model


def CreateRNN(name, X, Y, tokenizer, maxWordsCount = 5000, sequences_len = 100, batch_size = 64, epochs = 50):

    X = tokenizer.texts_to_sequences(X)
    Y = tokenizer.texts_to_sequences(Y)

    qa_pairs = [(X_seq, Y_seq) for X_seq, Y_seq in zip(X, Y)]

    train_pairs, test_pairs = train_test_split(qa_pairs, test_size = 0.2)

    X = pad_sequences([pair[0] for pair in train_pairs], maxlen = sequences_len, padding = 'post')
    Y = pad_sequences([pair[1] for pair in train_pairs], maxlen = sequences_len, padding = 'post')

    X = pad_sequences([pair[0] for pair in test_pairs], maxlen = sequences_len, padding = 'post')
    Y = pad_sequences([pair[1] for pair in test_pairs], maxlen = sequences_len, padding = 'post')

    Y = to_categorical(Y, num_classes = maxWordsCount)
    Y = to_categorical(Y, num_classes = maxWordsCount)

    model = Sequential()
    model.add(Embedding(maxWordsCount, 512, input_length = sequences_len))
    model.add(GRU(128, return_sequences = True))
    model.add(GRU(64, return_sequences = True))
    model.add(GRU(32, return_sequences = True))
    model.add(GRU(64))
    model.add(Dense(maxWordsCount, activation = 'softmax'))

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    model.summary()

    model.fit(X, Y, epochs = epochs, batch_size = batch_size, validation_data = (X, Y))

    save_RNN_model(name, model)

    return model

    

