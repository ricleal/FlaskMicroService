r'''
Flask RESTFull: using flask_restful package
This is the example that will folow us throughout the tutorial
'''

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse

from datetime import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('book', type=dict)

##############################################################################
# SQL
Base = declarative_base()

books_authors_table = db.Table(
    'books_authors', Base.metadata,
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)


class Book(Base):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    isbn = db.Column(db.String(32), nullable=True)
    published_date = db.Column(db.DateTime, nullable=True)
    authors = relationship(
        "Author",
        secondary=books_authors_table,
        back_populates="books")


class Author(Base):
    __tablename__ = 'author'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=True)
    last_name = db.Column(db.String(250), nullable=False)
    books = relationship(
        "Book",
        secondary=books_authors_table,
        back_populates="authors")


engine = db.create_engine('sqlite:///db.db')
# users.drop(engine) # drops the users table
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create authors
session.add_all([
    Author(first_name="John", last_name="Smith"),
    Author(first_name="John1", last_name="Smith1"),
    Author(first_name="John2", last_name="Smith2"),
    Author(first_name="John3", last_name="Smith3"),
    Author(first_name="John4", last_name="Smith4"),
])
session.commit()

authors = session.query(Author).filter(Author.first_name.in_(
    ['John', 'John1'])).all()

session.add(
    Book(title="title1", isbn="12345678", published_date=datetime.utcnow(),
         authors=authors)
)
session.commit()

authors = session.query(Author).filter(Author.first_name.in_(
    ['John2', 'John4'])).all()

session.add(
    Book(title="title2", isbn="464342323", published_date=datetime.utcnow(),
         authors=authors)
)
session.commit()

###


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
