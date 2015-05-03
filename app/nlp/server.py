import tornado.ioloop
import tornado.web
import tornado.wsgi
import nlp
import json
from nlp import *

class NounPhraseHandler(tornado.web.RequestHandler):
    def post(self):
        content = str(self.request.body)
        e = Extractor(content)
        self.write(str(json.dumps(e.noun_phrases())))

class TreeExtractorHandler(tornado.web.RequestHandler):
    def post(self):
        content = self.request.body
        e = TreeExtractor()
        self.write(json.dumps(e.tree(content)))

application = tornado.web.Application([
    (r"/extract/noun-phrases", NounPhraseHandler),
    (r"/extract/tree", TreeExtractorHandler),
])

wsgiapp = tornado.wsgi.WSGIAdapter(application)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
