from nlp.db import *
from nlp.processors import *

def random_text():
    import os
    import io
    import glob
    import random
    import codecs
    directory = random.choice(glob.glob("/training-data/journals/med/*"))
    filename = random.choice(glob.glob(directory + "/*"))
    return codecs.open(filename, 'rU', encoding='utf-8-sig', errors='replace').read().replace(" s ", "s ")
