import numpy as np

from keras.preprocessing.sequence import pad_sequences

def Word_level_QA_answer(model, tokenizer, msg, sequences_len = 100, answer_len = 100):

    input_seq = tokenizer.texts_to_sequences([msg])
    #try remove pad_sequences need to test how it will be works
    #input_seq = pad_sequences(input_seq, maxlen = sequences_len)

    predicted_probabilities = model.predict([input_seq, input_seq])

    res = ""

    for i in predicted_probabilities[0]:
        if np.argmax(i) != 0 and np.argmax(i) < len(tokenizer.index_word):
            res += tokenizer.index_word[np.argmax(i)] + " "

    return res


def Word_level_RNN_answer(model, tokenizer, msg, sequences_len = 100, answer_len = 100):

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

        if indx != 0 and indx < len(tokenizer.index_word):
            res += " " + tokenizer.index_word[indx]
    
    return res


def word_level_prerpocessing(X, Y, tokenizer, sequences_len):

    res = []

    for i in range(len(X)):
        X_pad = ""
        words = X[i].split()

        if len(words) > sequences_len:
            for i in range(sequences_len):
                X_pad += " " + words[i]
        else:
            X_pad = X[i]
        
        X_data = tokenizer.texts_to_sequences([X_pad])[0]

        if len(words) < sequences_len:
            while len(X_data) < sequences_len:
                X_data = [0] + X_data

        Y_pad = ""
        words = Y[i].split()

        if len(words) > sequences_len:
            for i in range(sequences_len):
                Y_pad += " " + words[i]
        else:
            Y_pad = X[i]
        
        Y_data = tokenizer.texts_to_sequences([Y_pad])[0]

        if len(words) < sequences_len:
            while len(Y_data) < sequences_len:
                Y_data = Y_data + [0]

        res.append(X_data + Y_data)

    return res 

