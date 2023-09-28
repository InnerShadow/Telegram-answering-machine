import io
import json

from keras.preprocessing.text import Tokenizer, tokenizer_from_json

#Save tokinazer with pre-coded name
def save_tokinazer(name, tokinazer):
    tokenizer_json = tokinazer.to_json()
    with io.open("Data/" + str(name) + '_tokenizer.json', 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(tokenizer_json, ensure_ascii = False))


#Load tokinazer just by users name
def load_tokinazer(name):
    with open("Data/" + str(name) + '_tokenizer.json') as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)

    return tokenizer


#Load tokinazer by full path
def full_path_load_tokinazer(name):
    with open(name) as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)

    return tokenizer


#Get Tokinazer by models name
def get_Tokinazer_by_model(model_name):
    return model_name[:len(model_name) - 6] + "_tokenizer.json"


#Create & get new tokinazer
def get_Tokinazer(X, Y, maxWordsCount = 5000, lower = True, char_level = False):
    tokenizer = Tokenizer(num_words = maxWordsCount, lower = lower, split = ' ', 
                          char_level = char_level, filters = '!–"—#$%&amp;()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r«»…')
    tokenizer.fit_on_texts(X + Y)
    return tokenizer

