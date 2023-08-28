import pickle

from keras.preprocessing.text import Tokenizer

def save_tokinazer(name, tokinazer):
    with open(str(name) + '_tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokinazer, handle, protocol = pickle.HIGHEST_PROTOCOL)


def load_tokinazer(name):
    with open(str(name) + '_tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    return tokenizer


def get_Tokinazer(X, Y, maxWordsCount = 5000, lower = True, char_level = False):
    
    tokenizer = Tokenizer(num_words = maxWordsCount, lower = lower, split = ' ', char_level = char_level, filters = '.,!?:-')
    tokenizer.fit_on_texts(X + Y)
    return tokenizer

