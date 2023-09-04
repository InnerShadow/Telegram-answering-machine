import pickle

from keras.preprocessing.text import Tokenizer

def save_tokinazer(name, tokinazer):
    with open("Data/" + str(name) + '_tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokinazer, handle, protocol = pickle.HIGHEST_PROTOCOL)


def load_tokinazer(name):
    with open("Data/" + str(name) + '_tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    return tokenizer


def full_path_load_tokinazer(name):
    with open(name, 'rb') as handle:
        tokenizer = pickle.load(handle)

    return tokenizer


def get_Tokinazer(X, Y, maxWordsCount = 5000, lower = True, char_level = False):
    
    tokenizer = Tokenizer(num_words = maxWordsCount, lower = lower, split = ' ', char_level = char_level, filters = '.,!?:-')
    tokenizer.fit_on_texts(X + Y)
    return tokenizer

def get_Tokinazer_by_model(model_name):
    return model_name[:len(model_name) - 3] + "_tokenizer.pickle"