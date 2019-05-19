#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)


class BookDAO(object):
    '''
    Data Access Object
    Class that manages the books in MongoDB
    We exclude the mongodb '_id' in the return value
    '''

    def __init__(self):
        client = MongoClient()
        db = client.testdb
        self.book_collection = db.books

    def get(self, id):
        book = self.book_collection.find_one({'id': id}, {'_id': False})
        return book

    def create(self, data):
        result = self.book_collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, id, data):
        result = self.book_collection.update_one({'id': id}, {"$set": data})
        return result.matched_count

    def delete(self, id):
        result = self.book_collection.delete_one({'id': id})
        return result.deleted_count

    def get_all(self):
        '''This probably needs to be paginated, TODO!'''
        book_list = list(self.book_collection.find({}, {'_id': False}))
        return book_list


parser = reqparse.RequestParser()
parser.add_argument('book', type=dict)

dao = BookDAO()


class Book(Resource):
    '''
    Class that handles REST for '/books/<int:book_id>'
    get, delete and put (update)
    '''

    def get(self, book_id):
        book = dao.get(book_id)
        if book is None:
            abort(404, message="Book {} doesn't exist".format(book_id))
        else:
            return book

    def delete(self, book_id):
        deleted_items = dao.delete(book_id)
        if deleted_items is None:
            abort(404, message="Book {} doesn't exist".format(book_id))
        else:
            # Delete returns allways empty?
            return '', 204

    def put(self, book_id):
        args = parser.parse_args()
        data = args['book']
        matched_count = dao.update(book_id, data)
        return {'matched_count': matched_count}, 201


class BookList(Resource):
    ''' shows a list of all Books, and lets you POST to add new tasks '''

    def get(self):
        books = dao.get_all()
        return books

    def post(self):
        # json_data = request.get_json(force=True)
        args = parser.parse_args()
        inserted_id = dao.create(args['book'])
        return {'inserted_id': inserted_id}, 201


api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<int:book_id>')


if __name__ == '__main__':
    app.run(debug=True)
