#!/usr/bin/python3
import json
import os

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)


def get_schema_as_dict(filename=os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'infered_schema.json')):
    ''' Parses the filename and builds a dictionary from json '''
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


ns = api.namespace('books', description='Book operations')
book = api.schema_model('Book', get_schema_as_dict())


class BookDAO(object):
    ''' Class that manages the books in MongoDB '''

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

    def get_all_books(self):
        ''' BSON Serialised because of the ObjectId'''
        book_list = list(self.book_collection.find({}).limit(10))
        #return [book for book in self.book_collection.find({}).limit(10)]
        return json.dumps(book_list, default=json_util.default)


dao = BookDAO()


@ns.route('/')
class BookList(Resource):
    '''Shows a list of all books, and lets you POST to add new books'''

    #@ns.marshal_list_with(book)
    def get(self):
        '''List all books'''
        return dao.get_all_books()

    @ns.expect(book)
    @ns.marshal_with(book, code=201)
    def post(self):
        '''Create a new book'''
        return dao.create(api.payload), 201


@ns.route('/<string:id>')
@ns.response(404, 'Book not found')
@ns.param('id', 'The Book BSON identifier')
class Book(Resource):
    '''Show a single book item and lets you delete them'''

    @ns.doc('get_book')
    # @ns.marshal_with(book)
    @ns.expect(book)
    def get(self, id):
        '''Fetch a given book'''
        return dao.get(id)

    @ns.doc('delete_book')
    @ns.response(204, 'book deleted')
    def delete(self, id):
        '''Delete a book given its ObjectId'''
        dao.delete(id)
        return '', 204

    @ns.expect(book)
    @ns.marshal_with(book)
    def put(self, id):
        '''Update a task given its ObjectId'''
        return dao.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
