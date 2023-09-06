import numpy as np

from keras.models import Model
from keras.layers import Dense, Embedding, LSTM, GRU, Input
from keras.models import load_model
from keras.utils import to_categorical

from keras.preprocessing.sequence import pad_sequences


def save_QA_model(name, model):
    model.save("Data/" + str(name) + ".h5")


def load_QA_model(name):
    model = load_model("Data/" + str(name) + ".h5")
    return model


def full_path_load_QA_model(name):
    model = load_model(name)
    return model


def QA_model_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack, DoMaxPackLen = False):
    for i in range(epochs):
        index = 0
        loss_values = []
        accuracy_values = []
        print("epoch " + str(i) + " from " + str(epochs))
        for j in range(int(len(X) / messages_per_pack)):
            Q = []
            A = []
            for k in range(index, index + messages_per_pack):
                if k >= len(X):
                    break

                Q.append(X[k])
                A.append(Y[k])

            #TODO: Test maxLen
            if DoMaxPackLen:
                maxLen = max(
                    max(map(len, A)),
                    max(map(len, Q))
                )
                sequences_len = maxLen

            data_X = pad_sequences(tokenizer.texts_to_sequences(Q), maxlen = sequences_len)
            data_Y = pad_sequences(tokenizer.texts_to_sequences(A), maxlen = sequences_len)
            

            Y_categorical = to_categorical(data_Y, num_classes=maxWordsCount)

            index += batch_size

            history = model.fit([data_X, data_X], Y_categorical, batch_size = batch_size)

            loss_values.append(history.history['loss'])
            accuracy_values.append(history.history['accuracy'])

        print("Mean loss: " + str(np.sum(loss_values) / len(loss_values)) + " mean accuracy: " + str(np.sum(accuracy_values) / len(accuracy_values)) + str("\n"))

    return model


def Get_RNN_QA(maxWordsCount = 5000, latent_dim = 256):
    shared_embedding_layer = Embedding(maxWordsCount, latent_dim)

    encoder_inputs = Input(shape = (None, ))
    decoder_inputs = Input(shape = (None, ))

    encoder_embedding = shared_embedding_layer(encoder_inputs)
    decoder_embedding = shared_embedding_layer(decoder_inputs)

    encoder_lstm = LSTM(latent_dim, return_sequences = True, return_state = True)
    encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)
    encoder_states = [state_h, state_c]

    decoder_lstm = LSTM(latent_dim, return_sequences = True, return_state = True)
    decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)

    decoder_dense = Dense(maxWordsCount, activation = 'softmax')
    decoder_outputs = decoder_dense(decoder_outputs)

    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

    model.summary()
    return model

