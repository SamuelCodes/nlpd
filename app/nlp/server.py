# encoding=utf8
import web
import nlp
import json
from nlp import *

urls = (
    '/extract/noun-phrases', 'ExtractNounPhrases'
)

app = web.application(urls, globals())
wsgiapp = app.wsgifunc()

class ExtractNounPhrases:
    def POST(self):
        data = unicode(web.data())
        extractor = Extractor(data)
        web.header('Content-Type', 'application/json')
        return json.dumps(extractor.noun_phrases())
