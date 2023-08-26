import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import random
import matplotlib.pyplot as plt
import tensorflow as tf
import glob
import re

from PIL import Image
from random import randint
from tensorflow import keras
from keras.datasets import mnist
from keras.layers import Dense, SimpleRNN, Input, Dropout, Embedding
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb
from skimage.io import imsave
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical


def CreateRNN(name, X, Y, inp_words = 20, maxWordsCount = 10000, lower = True, char_level = False):

    texts = []

    for i in X:
        texts.extend(re.split(r'[ .,!?\n]', i))

    for i in Y:
        texts.extend(re.split(r'[ .,!?\n]', i))

    tokenizer = Tokenizer(num_words=maxWordsCount, lower=lower, split=' ', char_level=char_level, filters='')
    tokenizer.fit_on_texts(texts)

    #dlist = list(tokenizer.word_counts.items())
    #print(dlist[:100])
