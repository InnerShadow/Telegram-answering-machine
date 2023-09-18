import numpy as np

from keras.preprocessing.sequence import pad_sequences

#Generate answer from input string
def Word_level_QA_answer(model, tokenizer, msg, contexts, sequences_len = 25):
    #Reshape sentenses
    input_seq = tokenizer.texts_to_sequences([msg])
    input_seq = pad_sequences(input_seq, maxlen = sequences_len)

    #Reshape contexts
    contexts_seq = tokenizer.texts_to_sequences([contexts])
    contexts_seq = pad_sequences(contexts_seq, maxlen = sequences_len * 3)

    predicted_probabilities = model.predict([input_seq, input_seq, contexts_seq])

    res = ""

    #Collect answer
    #Get prev not to repeat words
    prev = 0
    for i in predicted_probabilities[0]:
        if prev != np.argmax(i): 
            if np.argmax(i) != 0 and np.argmax(i) < len(tokenizer.index_word):
                res += tokenizer.index_word[np.argmax(i)] + " "

        prev = np.argmax(i)

    return res

