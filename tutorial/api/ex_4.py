r'''
Flask RESTFull: using flask_restful package and jsonschema for validation
Create a decorator to validate
'''

from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse
from .bookshelf import BookShelf
from jsonschema import validate
from jsonschema.exceptions import ValidationError

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "required": [
        "id",
        "title",
    ],
    "properties": {
        "id": {
            "type": "integer"
        },
        "title": {
            "type": "string"
        },
        "isbn": {
            "type": "string"
        },
        "published_date": {
            "type": "string"
        },
        "authors": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
    },
    "additionalProperties": False
}


def validator_decorator(func):
    ''' Validator decorator to use in Flask '''
    def func_wrapper(*args, **kwargs):
        json_data = request.get_json(force=True)
        try:
            validate(instance=json_data['book'], schema=schema)
        except ValidationError:
            return abort(422)
        return func(*args, **kwargs)
    return func_wrapper


app = Flask(__name__)
api = Api(app)

dao = BookShelf()

parser = reqparse.RequestParser()
parser.add_argument('book', type=dict)


class Book(Resource):
    '''
    Class that handles REST for '/books/<int:book_id>'
    get, delete and put (update)
    '''

    def get(self, book_id):
        book = dao.get(book_id)
        if not book:
            abort(404, message="Book {} doesn't exist".format(book_id))
        else:
            return book

    def delete(self, book_id):
        try:
            dao.delete(book_id)
            return '', 204
        except KeyError:
            abort(404, message="Book {} doesn't exist".format(book_id))

    def put(self, book_id):
        try:
            args = parser.parse_args()
            data = args['book']
            dao.update(book_id, data)
            return '', 201
        except KeyError:
            abort(404, message="Book {} doesn't exist".format(book_id))


class BookList(Resource):
    ''' shows a list of all Books, and lets you POST to add new tasks '''

    def get(self):
        return dao.get_all()

    @validator_decorator
    def post(self):
        '''
        curl -X PUT -H "Content-Type: application/json" \
        -d '{ "book": { "id": 10, "title": "Test Book 1", \
            "isbn": "9781234567897", "published_date": "2019-04-13", \
            "authors": [ "Rea Horne", "Cristiano Searle" ] } }' \
        http://127.0.0.1:5000/books
        '''
        args = parser.parse_args()
        dao.create(args['book'])
        return '', 201


api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<int:book_id>')


if __name__ == '__main__':
    app.run(debug=True)
