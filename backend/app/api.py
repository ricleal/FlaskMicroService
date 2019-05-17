#!/usr/bin/python3
import json
import os

from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask
from flask_restplus import fields, Api, Resource

app = Flask(__name__)
api = Api(app)

def get_schema_as_dict(filename=os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'infered_schema.json')):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

book = api.schema_model('Book', get_schema_as_dict())

class BookDAO(object):
    def __init__(self):
        client = MongoClient()
        db = client.testdb
        self.book_collection = db.books

    def get(self, id):
        if type(id) == str:
            id = ObjectId(id)
        book = self.book_collection.find_one({'_id': id})
        if book:
            return book
        else:
            api.abort(404, "Book with _id = {} doesn't exist".format(id))

    def create(self, data):
        result = self.book_collection.insert_one(data)
        return result.inserted_id

    def update(self, id, data):
        if type(id) == str:
            id = ObjectId(id)
        result = self.book_collection.update_one({'_id': id}, {"$set": data})
        return result.matched_count

    def delete(self, id):
        result = self.book_collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count


if __name__ == '__main__':
    app.run(debug=True)
