import numpy as np
import matplotlib.pyplot as plt

from keras.models import Model
from keras.layers import Dense, Embedding, Input, LSTM, Attention, Concatenate, RepeatVector, Lambda
from keras.models import load_model
from keras.utils import to_categorical
from keras.optimizers import Adam

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
def QA_model_train(name, model, X, Y, tokenizer, batch_size, epochs, sequences_len, maxWordsCount, messages_per_pack):
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

            contects = []

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

                #Fill context array
                current_context = ""
                offset = 0
                while len(current_context.split(" ")) <= 2 * sequences_len:
                    if k - offset < 0:
                        break

                    current_context = current_context + X[k - offset] + ". " + Y[k - offset] + ". "
                    offset += 1 

                contects.append(current_context)

            #Convert messeges to numbers sequences
            data_X = pad_sequences(tokenizer.texts_to_sequences(Q), maxlen = sequences_len)
            data_Y = pad_sequences(tokenizer.texts_to_sequences(A), maxlen = sequences_len)

            #Get cotext sequences
            data_cotext = pad_sequences(tokenizer.texts_to_sequences(contects), maxlen = sequences_len * 2)
            
            #Get one-hot encoding vector to Y (Answer's) list
            Y_categorical = to_categorical(data_Y, num_classes = maxWordsCount)

            #Increase index
            index += messages_per_pack
            
            #Get loss & accuracy and train model by cuurent pack of messeges
            history = model.fit([data_X, data_X, data_cotext], Y_categorical, batch_size = batch_size)

            #Save loss & accuracy valus
            loss_values.append(history.history['loss'])
            accuracy_values.append(history.history['accuracy'])

        print("Mean loss: " + str(np.sum(loss_values) / len(loss_values)) + "; Mean accuracy: " + str(np.sum(accuracy_values) / len(accuracy_values)) + str("\n"))
        global_loss.append((np.sum(loss_values) / len(loss_values)))

    #Show & save graphs
    plt.plot(global_loss)
    plt.show()
    plt.savefig("Data/" + name + "_graph.png")

    return model


#Creates seq2seq NN
def Get_RNN_QA(maxWordsCount = 10000, latent_dim = 200, sequences_len = 20, context_weight = 0.3):

    #Encoder input layer
    encoder_inputs = Input(shape = (sequences_len, ))

    #Encoder embedding
    encoder_embedding = Embedding(maxWordsCount, latent_dim)(encoder_inputs)

    #LSTM layer for Encoder
    encoder_lstm = LSTM(latent_dim, return_sequences = True, return_state = True)
    encoder_outputs, encoder_state_h, encoder_state_c = encoder_lstm(encoder_embedding)

    #Input Decoder layer
    decoder_inputs = Input(shape = (sequences_len, ))

    #Decoder embedding
    decoder_embedding = Embedding(maxWordsCount, latent_dim)(decoder_inputs)

    #LSTM Decoder Layer
    decoder_lstm = LSTM(latent_dim, return_sequences = True, return_state = True)
    decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state = [encoder_state_h, encoder_state_c])

    #Attention layer
    attention_layer = Attention()([decoder_outputs, encoder_outputs])

    #Concatenate attention output with decoder outputs
    decoder_combined_context = Concatenate(axis = -1)([decoder_outputs, attention_layer])

    
    #Get count contest lstm dims
    context_lstm_dims = 0
    if latent_dim < 4:
        context_lstm_dims = 1
    else :
        context_lstm_dims = latent_dim // 4

    #Add context input
    context_inputs = Input(shape = (sequences_len * 2, ))
    context_embedding = Embedding(maxWordsCount, context_lstm_dims)(context_inputs)

    context_lstm = LSTM(context_lstm_dims)(context_embedding)

    #Multiply context representation by a weight
    weighted_context = Lambda(lambda x: x * context_weight)(context_lstm)

    #Repeat the context vector to match sequences_len
    repeated_context = RepeatVector(sequences_len)(weighted_context)

    #Concatenate context vector with decoder outputs and attention
    decoder_combined_context_context = Concatenate(axis = -1)([decoder_combined_context, repeated_context])

    #Decoder output
    decoder_dense = Dense(maxWordsCount, activation = 'softmax')
    decoder_outputs = decoder_dense(decoder_combined_context_context)

    #Connect decoder, encoder, and context inputs
    model = Model([encoder_inputs, decoder_inputs, context_inputs], decoder_outputs)

    #Compile model
    model.compile(optimizer = Adam(learning_rate = 0.001), loss = 'categorical_crossentropy', metrics = ['accuracy'])

    model.summary()

    return model

