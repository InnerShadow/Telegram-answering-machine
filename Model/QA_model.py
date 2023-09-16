import numpy as np
import matplotlib.pyplot as plt

from keras.models import Model
from keras.layers import Dense, Embedding, Input, LSTM, Attention, Concatenate
from keras.models import load_model
from keras.utils import to_categorical
from keras.optimizers import Adadelta

from keras.preprocessing.sequence import pad_sequences

#Save QA model
def save_QA_model(name, model):
    model.save("Data/" + str(name) + ".h5")


#Load QA model by name of victim
def load_QA_model(name):
    model = load_model("Data/" + str(name) + ".h5")
    return model


#Get QA model by full path
def full_path_load_QA_model(name):
    model = load_model(name)
    return model


#Train Qa model step by step
def QA_model_train(model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack):
    #Save loss for graphics
    global_loss = []
    #For by num of epochs
    for i in range(epochs):
        #Reser index value
        index = 0
        #Reset loass & accuracy stats
        loss_values = []
        accuracy_values = []
        print("epoch " + str(i) + " from " + str(epochs))
        for j in range(int(len(X) / messages_per_pack)):
            #Reset Question & Answer lists
            Q = []
            A = []

            #Make pad to get up to 10% of 'messages_per_pack' to catch pad number of messages from prev pack for better trainig.
            pad = np.random.randint(0, int(0.1 * messages_per_pack))

            for k in range(index - pad, index + messages_per_pack):
                
                if k < 0:
                    continue

                if k >= len(X):
                    break
                
                #Fill Question & Answer lists
                Q.append(X[k])
                A.append(Y[k])

            #Convert messeges to numbers sequences
            data_X = pad_sequences(tokenizer.texts_to_sequences(Q), maxlen = sequences_len)
            data_Y = pad_sequences(tokenizer.texts_to_sequences(A), maxlen = sequences_len)
            
            #Get one-hot encoding vector to Y (Answer's) list
            Y_categorical = to_categorical(data_Y, num_classes = maxWordsCount)

            #Increase index
            index += messages_per_pack
            
            #Get loss & accuracy and train model by cuurent pack of messeges
            history = model.fit([data_X, data_X], Y_categorical, batch_size = batch_size)

            #Save loss & accuracy valus
            loss_values.append(history.history['loss'])
            accuracy_values.append(history.history['accuracy'])

        print("Mean loss: " + str(np.sum(loss_values) / len(loss_values)) + "; Mean accuracy: " + str(np.sum(accuracy_values) / len(accuracy_values)) + str("\n"))
        global_loss.append((np.sum(loss_values) / len(loss_values)))

    #Show graphs
    plt.plot(global_loss)
    plt.show()

    return model


#Creates seq2seq NN
def Get_RNN_QA(maxWordsCount = 10000, latent_dim = 200, sequences_len = 20):

    # Adjusted dimensions
    half_dim = latent_dim // 2
    quarter_dim = latent_dim // 4

    # Encoder input layer
    encoder_inputs = Input(shape = (sequences_len, ))

    # Encoder embedding
    encoder_embedding = Embedding(maxWordsCount, latent_dim)(encoder_inputs)

    # LSTM layer for Encoder
    encoder_lstm = LSTM(latent_dim, return_sequences = True, return_state = True)
    encoder_outputs, encoder_state_h, encoder_state_c = encoder_lstm(encoder_embedding)

    # Additional LSTM and Dense layer
    encoder_lstm2 = LSTM(half_dim, return_sequences = True, return_state = True)
    encoder_outputs2, _, _ = encoder_lstm2(encoder_outputs)

    dense_layer1 = Dense(quarter_dim, activation = 'relu')
    encoder_outputs2 = dense_layer1(encoder_outputs2)

    # Input Decoder layer
    decoder_inputs = Input(shape = (sequences_len, ))

    # Decoder embedding
    decoder_embedding = Embedding(maxWordsCount, latent_dim)(decoder_inputs)

    # LSTM Decoder Layer
    decoder_lstm = LSTM(latent_dim, return_sequences = True, return_state = True)
    decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state = [encoder_state_h, encoder_state_c])

    # Additional LSTM and Dense layer
    decoder_lstm2 = LSTM(half_dim, return_sequences = True, return_state = True)
    decoder_outputs2, _, _ = decoder_lstm2(decoder_outputs)

    dense_layer2 = Dense(quarter_dim, activation = 'relu')
    decoder_outputs2 = dense_layer2(decoder_outputs2)

    # Attention layer
    attention_layer = Attention()([decoder_outputs2, encoder_outputs2])

    # Concatenate attention output with decoder outputs
    decoder_combined_context = Concatenate(axis = -1)([decoder_outputs2, attention_layer])

    # Decoder output
    decoder_dense = Dense(maxWordsCount, activation = 'softmax')
    decoder_outputs = decoder_dense(decoder_combined_context)

    # Connect decoder & encoder
    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

    # Compile model
    model.compile(optimizer=Adadelta(), loss = 'categorical_crossentropy', metrics = ['accuracy'])

    model.summary()

    return model
