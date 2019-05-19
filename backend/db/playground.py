#!/usr/bin/python3
from pymongo import MongoClient
from pprint import pprint
# This is the same as 'mongodb://localhost:27017/'
client = MongoClient()

with client:
    db = client.testdb

    # for book in db.books.find():
    #     print(book['title'])
    
    book = db.books.find_one({'id': 1}, {'_id': False})
    pprint(book)
