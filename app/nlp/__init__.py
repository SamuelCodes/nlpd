from nlp.corpora import *
from nlp.extractors import *

def random_text():
    import os
    import io
    import glob
    import random
    import codecs
    directory = random.choice(glob.glob("/training-data/journals/med/*"))
    filename = random.choice(glob.glob(directory + "/*"))
    return codecs.open(filename, 'rU', encoding='utf-8-sig', errors='replace').read().replace(" s ", "s ")

def tokenized_sentences(text):
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    return [word_tokenize(s) for s in sent_tokenize(text)]

def random_sentences():
    return tokenized_sentences(random_text())
