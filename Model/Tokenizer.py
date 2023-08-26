from keras.preprocessing.text import Tokenizer

def get_Tokinazer(X, Y, maxWordsCount = 5000, lower = True, char_level = False,):
    
    tokenizer = Tokenizer(num_words = maxWordsCount, lower = lower, split = ' ', char_level = char_level, filters = '.,!?:-')
    tokenizer.fit_on_texts(X + Y)
    return tokenizer

