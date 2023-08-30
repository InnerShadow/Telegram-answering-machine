import numpy as np

def Word_level_answer(model, tokenizer, msg, sequences_len = 100, answer_len = 100):

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

