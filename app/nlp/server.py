import tornado.ioloop
import tornado.web
import tornado.wsgi
import nlp
import json

class EvalExtractorHandler(tornado.web.RequestHandler):
    def post(self, docref):
        import ast
        collection, doc_id = docref.split('/')
        document = db()[collection].find_one({ '_id': ObjectId(doc_id) })
        content = self.request.body
        local_vars = { 'document': document }
        code = compile(ast.parse(content), '<input>', mode='exec')
        eval(code, globals(), local_vars)
        if 'json_output' in local_vars:
            self.write(json.dumps(local_vars['json_output']))
        else:
            self.write(json.dumps({'status': 'ok'}))

application = tornado.web.Application([
    (r"/eval/(.*)", EvalExtractorHandler),
])

wsgiapp = tornado.wsgi.WSGIAdapter(application)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
