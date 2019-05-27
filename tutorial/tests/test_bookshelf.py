import pytest
from api.bookshelf import BookShelf, content
import datetime


@pytest.fixture
def bookshelf():
    return BookShelf()


def test_get_all(bookshelf):
    assert bookshelf.get_all() == content


def test_get(bookshelf):
    assert [bookshelf.get(1)] == [b for b in content if b['id'] == 1]


def test_create(bookshelf):
    book = {
        "id": 10,
        "title": "Test Book 10",
        "isbn": "9781245567897",
        "published_date": datetime.date(2017, 4, 10).isoformat(),
        "authors": [
            "Lavinia Winters",
            "Colm Small",
        ]
    }
    bookshelf.create(book)
    assert bookshelf.get(10) == book


def test_update(bookshelf):
    book = {
        "title": "Title updated 123",
    }
    bookshelf.update(1, book)
    assert bookshelf.get(1)['title'] == book['title']
    with pytest.raises(KeyError):
        bookshelf.update(100, book)


def test_delete(bookshelf):
    bookshelf.delete(1)
    assert bookshelf.get(1) == []
    with pytest.raises(KeyError):
        bookshelf.delete(100)
