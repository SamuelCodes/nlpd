import io
import pymongo
from gzip import GzipFile
from bson.objectid import ObjectId

def db():
    from pymongo import MongoClient
    client = MongoClient('mongo')
    return client.gqstack_development

def get_document(doc_id):
    return db()['documents_bases'].find_one({'_id': ObjectId(doc_id)})

def get_text(doc_id):
    doc = get_document(doc_id)
    file_obj = io.BytesIO(doc['body'].decode('base64'))
    gz = GzipFile(fileobj=file_obj)
    return gz.read()


def get_all_tweets():
    for account in db()['contacts_accounts_accounts'].find({}):
        for tweet in account['tweets']:
            print("Processing tweet " + tweet['text'])
            yield tweet['text']
