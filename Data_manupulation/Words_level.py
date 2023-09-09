import numpy as np

from keras.preprocessing.sequence import pad_sequences

#Generate answer from input string
def Word_level_QA_answer(model, tokenizer, msg, sequences_len = 100):
    #Reshape sentenses
    input_seq = tokenizer.texts_to_sequences([msg])
    input_seq = pad_sequences(input_seq, maxlen = sequences_len)

    predicted_probabilities = model.predict([input_seq, input_seq])

    res = ""

    #Collect answer
    for i in predicted_probabilities[0]:
        if np.argmax(i) != 0 and np.argmax(i) < len(tokenizer.index_word):
            res += tokenizer.index_word[np.argmax(i)] + " "

    return res
