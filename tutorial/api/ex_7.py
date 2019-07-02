r'''
Flask RESTFull: using flask_restful package
This is the example that will folow us throughout the tutorial
'''

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from faker import Faker

app = Flask(__name__)
api = Api(app)

# Define this before to avoid warning!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

fake = Faker()

parser = reqparse.RequestParser()
parser.add_argument('book', type=dict)

##############################################################################
# SQL


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
        back_populates="books",
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

db.create_all()






class AuthorSchema(ModelSchema):
    class Meta:
        model = Author


class BookSchema(ModelSchema):

    authors = fields.Nested(
        AuthorSchema, many=True, exclude=("books",) # Exclude in the target model
    )

    class Meta:
        model = Book
        sqla_session = db.session


author_schema = AuthorSchema()
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


class BookResource(Resource):
    '''
    Class that handles REST for '/books/<int:book_id>'
    get, delete and put (update)
    '''

    def get(self, book_id):
        book = Book.query.get(book_id)
        result = book_schema.dump(book)
        return result.data

    def delete(self, book_id):
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return '', 204

    def put(self, book_id):
        abort(404, message="Not implemented")


class BookListResource(Resource):
    ''' shows a list of all Books, and lets you POST to add new tasks '''

    def get(self):
        all_books = Book.query.all()
        result = books_schema.dump(all_books)
        return result.data

    def post(self):
        '''
        curl -X POST -H "Content-Type: application/json" \
        -d '{ "book": {
            "published_date": "2019-06-02T18:21:54.171733+00:00", \
            "title": "Posted book.", \
            "authors": [4, 5], \
            "isbn": "5290923846941" \
            } \
        }' \
        http://127.0.0.1:5000/books
        '''
        args = parser.parse_args()
        obj_json = args['book']
        book = Book(**obj_json)
        db.session.add(book)
        db.session.commit()
        return '', 201


api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')


if __name__ == '__main__':
    app.run(debug=True)
