import numpy as np
import matplotlib.pyplot as plt

from keras.models import Model
from keras.layers import Dense, Embedding, LSTM, Input, Dropout, BatchNormalization, GRU
from keras.models import load_model
from keras.utils import to_categorical

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
            for k in range(index, index + messages_per_pack):
                if k >= len(X):
                    break
                
                #Fill Question & Answer lists
                Q.append(X[k])
                A.append(Y[k])

            #Convert messeges to numbers sequences
            data_X = pad_sequences(tokenizer.texts_to_sequences(Q), maxlen = sequences_len, padding = 'post')
            data_Y = pad_sequences(tokenizer.texts_to_sequences(A), maxlen = sequences_len, padding = 'post')
            
            #Get one-hot encoding vector to Y (Answer's) list
            Y_categorical = to_categorical(data_Y, num_classes = maxWordsCount)

            #Increase index
            index += messages_per_pack
            
            #Get loss & accuracy and train model by cuurent pack of messeges
            history = model.fit([data_X, data_X], Y_categorical, batch_size = batch_size)

            #Save loss & accuracy valus
            loss_values.append(history.history['loss'])
            accuracy_values.append(history.history['accuracy'])

        print("Mean loss: " + str(np.sum(loss_values) / len(loss_values)) + " mean accuracy: " + str(np.sum(accuracy_values) / len(accuracy_values)) + str("\n"))
        global_loss.append((np.sum(loss_values) / len(loss_values)))

    #Show graphs
    plt.plot(global_loss)
    plt.show()

    return model


#Creates seq2seq NN
def Get_RNN_QA(maxWordsCount = 5000, latent_dim = 256, sequences_len = 20):

    #Encoder input layer
    encoder_inputs = Input(shape = (sequences_len,))
    
    #Encoder embending
    encoder_embedding = Embedding(maxWordsCount, latent_dim)(encoder_inputs)
    
    #LSTM layer for Encoder
    encoder_lstm = LSTM(latent_dim, return_sequences = True, return_state = True)
    encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)
    encoder_states = [state_h, state_c]
    
    #Add BatchNormalization & Dropout for better training
    encoder_outputs = BatchNormalization()(encoder_outputs)
    encoder_outputs = Dropout(0.2)(encoder_outputs)

    #Encoder GRU layer
    encoder_gru = GRU(int(latent_dim / 2), return_sequences = True, return_state = True)
    encoder_outputs, encoder_state = encoder_gru(encoder_outputs)
    
    #Add BatchNormalization & Dropout for better training
    encoder_outputs = BatchNormalization()(encoder_outputs)
    encoder_outputs = Dropout(0.2)(encoder_outputs)

    #Input Decoder layer
    decoder_inputs = Input(shape=(sequences_len,))
    
    #Decodere embenging
    decoder_embedding = Embedding(maxWordsCount, latent_dim)(decoder_inputs)
    
    #LSTM Decoder Layer 
    decoder_lstm = LSTM(latent_dim, return_sequences = True, return_state = True)
    decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state = encoder_states)
    
    #Add BatchNormalization & Dropout for better training
    decoder_outputs = BatchNormalization()(decoder_outputs)
    decoder_outputs = Dropout(0.2)(decoder_outputs)

    #GRU Decoder Layer 
    decoder_gru = GRU(int(latent_dim / 2), return_sequences = True, return_state = True)
    decoder_outputs, _ = decoder_gru(decoder_outputs, initial_state = encoder_state)
    
    #Add BatchNormalization & Dropout for better training
    decoder_outputs = BatchNormalization()(decoder_outputs)
    decoder_outputs = Dropout(0.2)(decoder_outputs)

    #Decoder output
    decoder_dense = Dense(maxWordsCount, activation = 'softmax')
    decoder_outputs = decoder_dense(decoder_outputs)

    #Conncect decoder & encoder
    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

    #Compile model
    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

    model.summary()

    return model
