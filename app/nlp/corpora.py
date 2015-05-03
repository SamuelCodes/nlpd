# encoding=utf8
import pdb
import uuid
import codecs
import os
import nltk
from gensim.models.lsimodel import LsiModel
from nltk.tokenize import word_tokenize, sent_tokenize

class Corpus(object):

    def __init__(self, name):
        self.name = name
        self.lemmatizer = nltk.WordNetLemmatizer()
        self.stemmer = nltk.stem.snowball.EnglishStemmer()
        self.model = None

    def tokenize(self, text):
        return [self.lemmatizer.lemmatize(self.stemmer.stem(w)) for w in word_tokenize(text)]

    def training_documents_from_path(self, path, extension=".txt"):
        for root, directories, filenames in os.walk(path):
            for file in filter(lambda file: file.endswith(extension), filenames):
                document = codecs.open(os.path.join(root, file), 'r', 'utf-8-sig', errors='replace').read()
                yield(self.tokenize(document))

    def from_text_files_in_path(self, path, extension=".txt"):
        doc_id = 0
        for tokens in self.training_documents_from_path(path, extension):
            document = { 'id': "doc_" + str(doc_id), 'tokens': tokens }
            doc_id = doc_id + 1
            if self.model:
                self.model.add_documents(document)
            else:
                self.model = LsiModel(document)
        return self.model
