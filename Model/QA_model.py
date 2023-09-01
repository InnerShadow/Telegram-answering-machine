
from keras.models import Model
from keras.layers import Dense, Embedding, LSTM, GRU, Input, Attention
from keras.models import Sequential, load_model
from keras.utils import to_categorical

from keras.preprocessing.sequence import pad_sequences


def save_QA_model(name, model):
    model.save("Data/QA_" + str(name[1:]) + ".h5")


def load_QA_model(name):
    model = load_model("Data/QA_" + str(name[1:]) + ".h5")
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

            model.fit(data_X, Y_categorical, )

    return model


def Get_RNN_QA(maxWordsCount = 5000, sequences_len = 100):

    encoder_inputs = Input(shape = (None, maxWordsCount))
    decoder_inputs = Input(shape = (None, maxWordsCount))

    encoder_lstm = LSTM(128, return_sequences = True, return_state = True)
    encoder_outputs, state_h, state_c = encoder_lstm(encoder_inputs)
    encoder_states = [state_h, state_c]

    attention_layer = Attention()([encoder_outputs, decoder_inputs])

    decoder_lstm = LSTM(128, return_sequences = True, return_state = True)
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)

    decoder_dense = Dense(maxWordsCount, activation = 'softmax')
    decoder_outputs = decoder_dense(decoder_outputs)

    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

    model.summary()

    return model
