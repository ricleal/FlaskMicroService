r'''
Flask RESTFull: using flask_restful package
This is the example that will folow us throughout the tutorial
'''

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from faker import Faker

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

fake = Faker()

parser = reqparse.RequestParser()
parser.add_argument('book', type=dict)

##############################################################################
# SQL

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'


books_authors_table = db.Table(
    'books_authors',
    db.Column('book_id', db.Integer, db.ForeignKey(
        'book.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey(
        'author.id'), primary_key=True),
)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    isbn = db.Column(db.String(32), nullable=True)
    published_date = db.Column(db.DateTime, nullable=True)
    authors = db.relationship(
        "Author",
        secondary=books_authors_table,
        back_populates="books"
    )

    def __repr__(self):
        return '<Book %r>' % self.title


class Author(db.Model):
    __tablename__ = 'author'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=True)
    last_name = db.Column(db.String(250), nullable=False)
    books = db.relationship(
        "Book",
        secondary=books_authors_table,
        back_populates="authors"
    )

    def __repr__(self):
        return '<Author %r>' % self.last_name


class BookSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('title', 'isbn', 'authors')


book_schema = BookSchema()
books_schema = BookSchema(many=True)


first_names = [fake.first_name() for _ in range(2)]

# Create authors
db.session.add_all([
    Author(first_name=first_names[0], last_name=fake.last_name()),
    Author(first_name=first_names[1], last_name=fake.last_name()),
    Author(first_name=fake.first_name(), last_name=fake.last_name()),
    Author(first_name=fake.first_name(), last_name=fake.last_name()),
    Author(first_name=fake.first_name(), last_name=fake.last_name()),
    Author(first_name=fake.first_name(), last_name=fake.last_name()),
])

db.session.commit()

authors = db.session.query(Author).filter(Author.first_name.in_(
    first_names)).all()

db.session.add(
    Book(title=fake.sentence(nb_words=4), isbn=fake.msisdn(),
         published_date=datetime.utcnow(), authors=authors)
)
db.session.commit()

db.authors = db.session.query(Author).filter(Author.first_name.in_(
    first_names)).all()

db.session.add(
    Book(title=fake.sentence(nb_words=4), isbn=fake.msisdn(),
         published_date=datetime.utcnow(), authors=authors)
)
db.session.commit()

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
