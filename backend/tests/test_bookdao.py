from app.api import BookDAO
from pymongo import MongoClient
from werkzeug.exceptions import NotFound
import pytest


@pytest.fixture
def book_dao():
    return BookDAO()


@pytest.fixture
def book_id():
    client = MongoClient()
    with client:
        db = client.testdb
        book = db.books.find_one()
        return str(book['_id'])


def test_book_dao_get(book_dao, book_id):
    book = book_dao.get(book_id)
    assert book is not None


def test_book_create_update_delete(book_dao):
    data = {
        "title": "Test Book",
        "isbn": "1234",
        "pageCount": 520,
        "publishedDate": "2000-08-01T00:00:00.000-0700",
        "thumbnailUrl": "http://www.test.com/test.jpg",
        "longDescription": "",
        "status": "PUBLISH",
        "authors": [
            "Jonh Doe"
        ],
        "categories": [
            "Test 1",
            "Test 2",
        ]
    }
    # Insert
    inserted_id = book_dao.create(data)
    assert inserted_id is not None
    # Get
    book_fetched = book_dao.get(inserted_id)
    assert book_fetched is not None
    assert book_fetched['title'] == "Test Book"
    # update
    updated_count = book_dao.update(inserted_id, {"title": "Test Book 2"})
    assert updated_count == 1
    # Get
    book_fetched = book_dao.get(inserted_id)
    assert book_fetched is not None
    assert book_fetched['title'] == "Test Book 2"
    # Delete
    delete_count = book_dao.delete(inserted_id)
    assert delete_count == 1
    # Get
    with pytest.raises(NotFound):
        book_dao.get(inserted_id)
