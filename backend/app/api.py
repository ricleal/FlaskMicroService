#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from .book_dao import BookDAOMongo as BookDAO

app = Flask(__name__)
api = Api(app)

dao = BookDAO()

parser = reqparse.RequestParser()
parser.add_argument('book', type=dict)


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
            # HTTP Delete returns always empty?
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
