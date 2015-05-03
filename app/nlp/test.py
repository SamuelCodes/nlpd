from nlp.db import *
from nlp.extractors import *
from nlp.corpora import *

def test_twitter_extract(username):
    t=db().contacts_accounts_accounts.find_one({'username': username})
    tsents=[r['text'] for r in t['tweets']]
    te = TwitterFeatureExtractor()
    return te.extract(tsents)
