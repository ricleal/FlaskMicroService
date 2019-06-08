r'''
Flask RESTFull: using flask_restful package
With cache
'''
from operator import attrgetter

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse

from cachetools import LRUCache, TTLCache, cachedmethod

from .bookshelf import BookShelf

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

    # cache least recently used Python Enhancement Proposals
    cache_lru = LRUCache(maxsize=32)

    @cachedmethod(attrgetter('cache_lru'))
    def get(self, book_id):
        print("Calling <Book.get> book_id={}".format(book_id))
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

    # cache weather data for no longer than ten minutes
    cache_ttl = TTLCache(maxsize=1024, ttl=600)

    @cachedmethod(attrgetter('cache_ttl'))
    def get(self):
        print("Calling <BookList.get>")
        return dao.get_all()

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
