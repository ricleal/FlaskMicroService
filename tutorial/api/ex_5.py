import json
import os

from .bookshelf import BookShelf
from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app, version='0.1', title='Book API',
          description='A simple Book info API')


def get_schema_as_dict(filename=os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'schema.json')):
    ''' Parses the filename and builds a dictionary from json '''
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


# @ns.marshal_with does not work with schema_as_dict and nested json
# follow bug here: https://github.com/noirbizarre/flask-restplus/pull/640
ns = api.namespace('books', description='Book operations')
book_schema = api.schema_model('Book', get_schema_as_dict())

dao = BookDAO()


@ns.route('/<int:book_id>')
@ns.response(404, 'Book not found')
@ns.param('book_id', 'The Book ID identifier')
class Book(Resource):
    '''Show a single book item and lets you delete them'''

    # @ns.marshal_with(book_schema)
    def get(self, book_id):
        '''Fetch a given book'''
        return dao.get(book_id)

    @ns.response(204, 'Book deleted')
    def delete(self, book_id):
        '''Delete a book given its id'''
        deleted_items = dao.delete(book_id)
        print("Delete", deleted_items)
        if deleted_items >= 1:
            return '', 204
        else:
            api.abort(404, "Book {} doesn't exist".format(book_id))

    @ns.expect(book_schema)
    @ns.marshal_with(book_schema)
    def put(self, book_id):
        '''Update a task given its id'''
        return dao.update(id, api.payload['book'])


@ns.route('/')
class BookList(Resource):
    '''Shows a list of all books, and lets you POST to add new books'''

    # @ns.marshal_list_with(book_schema)
    def get(self):
        '''List all books'''
        return dao.get_all()

    @ns.expect(book_schema)
    # @ns.marshal_with(book_schema, code=201)
    def post(self):
        '''Create a new book
        example:
{
  "id":10001,
  "title":"Test Book",
  "isbn":"1234",
  "pageCount":520,
  "publishedDate":"2000-08-01T00:00:00.000-0700",
  "thumbnailUrl":"http://www.test.com/test.jpg",
  "longDescription":"",
  "status":"PUBLISH",
  "authors":[
    "Jonh Doe"
  ],
  "categories":[
    "Test 1",
    "Test 2"
  ]
}
        '''
        inserted_id = dao.create(api.payload)
        return {'inserted_id': inserted_id}, 201


if __name__ == '__main__':
    app.run(debug=True)
