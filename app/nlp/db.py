import pymongo
from bson.objectid import ObjectId

def db():
    from pymongo import MongoClient
    client = MongoClient('mongo')
    return client.gqstack_development

def get_document(collection, doc_id):
    return db()[collection].find_one({'_id': ObjectId(doc_id)})

def get_all_tweets():
    for account in db()['contacts_accounts_accounts'].find({}):
        for tweet in account['tweets']:
            print("Processing tweet " + tweet['text'])
            yield tweet['text']
