import tornado.ioloop
import tornado.web
import tornado.wsgi
import nlp
import json
from nlp import *

class AnalyzeHandler(tornado.web.RequestHandler):
    def post(self, docdef):
        collection, doc_id = docdef.split('/')
        print(collection)
        print(doc_id)

        doc = get_document(collection, doc_id)

        analysis = dict()
        at = AnalyzeText(doc['text'])

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

class EvalExtractorHandler(tornado.web.RequestHandler):
    def post(self, docref):
        import ast
        collection, doc_id = docref.split('/')
        document = db()[collection].find_one({ '_id': ObjectId(doc_id) })
        content = self.request.body
        local_vars = { 'document': document }
        code = compile(ast.parse(content), '<input>', mode='exec')
        eval(code, local_vars)
        if 'json_output' in local_vars:
            self.write(json.dumps(local_vars['json_output']))
        else:
            self.write(json.dumps({'status': 'ok'}))

application = tornado.web.Application([
    (r"/analyze/(.*)", AnalyzeHandler),
    (r"/extract/noun-phrases", NounPhraseHandler),
    (r"/extract/tree", TreeExtractorHandler),
    (r"/eval/(.*)", EvalExtractorHandler),
])

wsgiapp = tornado.wsgi.WSGIAdapter(application)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
