#!/usr/bin/python3
import json
import os

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

dir_path = os.path.dirname(os.path.realpath(__file__))

with client:

    db = client.testdb
    if not db.books or db.books.count() == 0:

        with open(os.path.join(dir_path, 'catalog.books.json')) as json_file:
            data = json.load(json_file)
            db.books.insert_many(data)

    print("DB books has {} entries.".format(db.books.count()))
