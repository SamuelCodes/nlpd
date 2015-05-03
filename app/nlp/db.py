import pymongo

def db():
    from pymongo import MongoClient
    client = MongoClient('mongo')
    return client.gqstack_development
