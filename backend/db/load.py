#!/usr/bin/python3
import json
import os

from bson import json_util
from pymongo import MongoClient

# Directory of this file
dir_path = os.path.dirname(os.path.realpath(__file__))

# This is the same as 'mongodb://localhost:27017/'
client = MongoClient()

with client:
    db = client.testdb
    if db.books or db.books.count_documents({}) > 0:
        print("Dropping the collection Books first...")
        db.books.drop()

    with open(os.path.join(dir_path, 'catalog.books.json')) as json_file:
        data = json.load(json_file, object_hook=json_util.object_hook)
        print("Adding to the collection Books")
        db.books.insert_many(data)

    print("DB books has {} entries.".format(db.books.count_documents({})))

    # for book in db.books.find():
    #     print(book['title'])
