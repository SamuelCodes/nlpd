import pattern
from pattern.en import *
from pattern.search import *


class NPExtract:

    def __init__(self, **kwargs):
        self.options = kwargs

    def __call__(self, tree):
        output = {}
        for m in search('NP', tree, STRICT):
            try:
                term = ' '.join([w.lemma for w in m.words])
                if term in output:
                    output[term] += 1
                else:
                    output[term] = 1
            except:
                print('Error encoding, skipping')
        return output


class DocumentProcessor:

    def __init__(self, text):
        self.text = text

    def process(self):
        output = { 'terms': None }
        tree = parsetree(self.text, lemmata=True, relations=True)
        npe = NPExtract()
        output['terms'] = npe(tree)
        return output


