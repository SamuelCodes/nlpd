import nltk
import gensim
import re
import itertools
from nltk.probability import *
from nltk import word_tokenize, sent_tokenize
from nltk import Tree

def tree2dict(tree):
    return {tree.label(): [tree2dict(t)  if isinstance(t, Tree) else t
                        for t in tree]}


class DefaultPreprocessor:

    def __init__(self, text):
        self.text = text
        self.stemmer = nltk.stem.WordNetLemmatizer()
        self.tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.append_stopwords()

    def append_stopwords(self):
        self.stopwords.append('rt')
        self.stopwords.append('&nbsp;')

    def acceptable_token(self, word):
        if word in self.stopwords: return False
        if len(word) <= 2: return False
        return True

    def sentences(self):
        return sent_tokenize(self.text)

    def normalize(self, word):
        return self.stemmer.lemmatize(word.lower())

    def tokenize(self, string):
        with_stopwords = [self.normalize(tok) for tok in self.tokenizer.tokenize(string)]
        return [word for word in with_stopwords if self.acceptable_token(word)]

    def tokenized_sentences(self):
        sents = [[word for word in self.tokenize(sent)] for sent in self.sentences()]
        bigram_t = gensim.models.Phrases(sents)
        trigram_t = gensim.models.Phrases(bigram_t[sents])
        return trigram_t[sents]

    def flattened_tokenized_sentences(self):
        sents = self.tokenized_sentences()
        return list(itertools.chain(*sents))

    def dictionary(self):
        return gensim.corpora.Dictionary(self.tokenized_sentences())

    def doc2bow_corpus(self):
        return [self.dictionary().doc2bow(text) for text in self.tokenized_sentences()]



class AnalyzeText:

    def __init__(self, text):
        self.text = text
        self.preprocessor = DefaultPreprocessor(self.text)
        self.dictionary = self.preprocessor.dictionary()
        self.corpus = self.preprocessor.doc2bow_corpus()

    def word2vec(self):
        return gensim.models.Word2Vec(self.preprocessor.tokenized_sentences())

    def freq_dist(self):
        return nltk.FreqDist(self.preprocessor.flattened_tokenized_sentences())

    def tfidf(self):
        return gensim.models.TfidfModel(self.corpus)

    def lsi(self):
        return gensim.models.LsiModel(self.tfidf_model[self.corpus], id2word=self.dictionary, num_topics=100)

    def analyze(self):
        return self.sentences


class TreeExtractor:
    def tree(self, text):
        from nltk.corpus import treebank
        t = treebank.parsed_sents([word_tokenize(s) for s in sent_tokenize(text)])
        return tree2dict(t)

class TwitterFeatureExtractor:
    def extract(self, corpus):
        from nltk.stem import WordNetLemmatizer
        from nltk.corpus import stopwords
        from nltk.tokenize import WhitespaceTokenizer
        exclude_words = stopwords.words('english')
        exclude_words.append('rt')
        exclude_words.append('&amp;')
        tok = WhitespaceTokenizer()
        lem = WordNetLemmatizer()
        tsents = [tok.tokenize(sent) for sent in corpus]
        norm_words = []
        for sent in tsents:
            for word in sent:
                if word.startswith('http://'): continue
                nword = lem.lemmatize(word.lower())
                if nword not in exclude_words:
                    norm_words.append(nword)
        return nltk.FreqDist(norm_words)

class Extractor:
    def __init__(self, corpus):
        self.corpus = re.sub(r" s[!\"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~$]", " ", corpus)

    def noun_phrases(self):
        return self.parse()

    def parse(self):
        sentence_re = r'''(?x)      # set flag to allow verbose regexps
              ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
            | \w+(-\w+)*            # words with optional internal hyphens
            | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
            | \.\.\.                # ellipsis
            | [][.,;"'?:-_`]      # these are separate tokens
        '''
        grammar = r"""
            NBAR:
                {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

            NP:
                {<NBAR>}
                {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
        """
        lemmatizer = nltk.WordNetLemmatizer()
        chunker = nltk.RegexpParser(grammar)
        toks = nltk.regexp_tokenize(self.corpus, sentence_re)
        postoks = nltk.tag.pos_tag(toks)
        tree = chunker.parse(postoks)

        from nltk.corpus import stopwords
        stopwords = stopwords.words('english')

        def leaves(tree):
            """Finds NP leaf nodes of a chunked tree."""
            for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
                yield subtree.leaves()

        def normalize(word):
            """lowercases and lemmatizes word."""
            word = word.lower()
            word = lemmatizer.lemmatize(word)
            return word

        def acceptable_term(term):
            return len(term) > 1

        def acceptable_word(word):
            return len(word) > 2

        def get_terms(tree):
            for leaf in leaves(tree):
                term = []
                for w,t in leaf:
                    if acceptable_word(w): term.append(normalize(w))
                if acceptable_term(term): yield term

        terms = get_terms(tree)
        noun_phrases = []

        for term in terms:
            noun_phrases.append(" ".join(term))

        fdist = FreqDist(noun_phrases)
        pdist = UniformProbDist(noun_phrases)

        unique_noun_phrases = []
        for np in noun_phrases:
            if np not in unique_noun_phrases:
                unique_noun_phrases.append(np)

        return [ { 'term': np, 'freq': fdist.freq(np), 'prob': pdist.prob(np), 'logprob': pdist.logprob(np) } for np in unique_noun_phrases ]
