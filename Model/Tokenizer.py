import io
import json

from keras.preprocessing.text import Tokenizer, tokenizer_from_json

def save_tokinazer(name, tokinazer):
    tokenizer_json = tokinazer.to_json()
    with io.open("Data/" + str(name) + '_tokenizer.json', 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(tokenizer_json, ensure_ascii = False))


def load_tokinazer(name):
    with open("Data/" + str(name) + '_tokenizer.json') as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)

    return tokenizer


def full_path_load_tokinazer(name):
    with open(name) as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)

    return tokenizer


def get_Tokinazer(X, Y, maxWordsCount = 5000, lower = True, char_level = False):
    
    tokenizer = Tokenizer(num_words = maxWordsCount, lower = lower, split = ' ', char_level = char_level, filters = '.,!?:-')
    tokenizer.fit_on_texts(X + Y)
    return tokenizer


def get_Tokinazer_by_model(model_name):
    return model_name[:len(model_name) - 3] + "_tokenizer.json"

