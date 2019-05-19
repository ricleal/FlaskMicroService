from app.api import BookDAO
import pytest


@pytest.fixture
def book_dao():
    return BookDAO()


@pytest.fixture
def book_id():
    return 100


def test_book_dao_get(book_dao, book_id):
    book = book_dao.get(book_id)
    assert book is not None


def test_book_create_update_delete(book_dao):
    data_id = 10001
    data = {
        "id": data_id,
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
    book_fetched = book_dao.get(data_id)
    assert book_fetched is not None
    assert book_fetched['title'] == "Test Book"
    # update
    updated_count = book_dao.update(data_id, {"title": "Test Book 2"})
    assert updated_count == 1
    # Get
    book_fetched = book_dao.get(data_id)
    assert book_fetched is not None
    assert book_fetched['title'] == "Test Book 2"
    # Delete
    delete_count = book_dao.delete(data_id)
    assert delete_count == 1
    # Get
    book_fetched = book_dao.get(data_id)
    assert book_fetched is None


def test_books_get_all(book_dao):
    # Get All
    books_fetched = book_dao.get_all()
    assert len(books_fetched) == 431
