from app.api import app
import pytest
import json


@pytest.fixture(scope="module")
def client():
    client = app.test_client()
    return client


def _get_response_data_as_dict(response):
    return json.loads(response.data.decode('utf8'))


def test_get_all(client):
    response = client.get('/books')
    assert len(_get_response_data_as_dict(response)) == 431


def test_book_create_update_delete(client):
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
    response = client.post('/books', data=json.dumps({"book": data}),
                           content_type='application/json')
    assert response.status_code == 201
    assert 'inserted_id' in _get_response_data_as_dict(response).keys()

    # Get inserted book
    response = client.get('/books/{}'.format(data_id))
    assert response.status_code == 200
    assert _get_response_data_as_dict(response)['title'] == "Test Book"

    # update
    response = client.put(
        '/books/{}'.format(data_id),
        data=json.dumps({"book": {"title": "Test Book 2"}}),
        content_type='application/json')
    assert response.status_code == 201
    assert 'matched_count' in _get_response_data_as_dict(response).keys()

    # Get updated book
    response = client.get('/books/{}'.format(data_id))
    assert response.status_code == 200
    assert _get_response_data_as_dict(response)['title'] == "Test Book 2"

    # delete inserted / update book
    response = client.delete(
        '/books/{}'.format(data_id),
        content_type='application/json')
    assert response.status_code == 204
    assert '' == response.data.decode('utf-8')

    # Get updated book
    response = client.get('/books/{}'.format(data_id))
    assert response.status_code == 404
    assert 'message' in _get_response_data_as_dict(response).keys()
    assert _get_response_data_as_dict(response)['message'] == \
        "Book {} doesn\'t exist".format(data_id)


def test_book_validation(client):

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
    response = client.post('/books', data=json.dumps({"book": data}),
                           content_type='application/json')
    assert response.status_code == 422
    assert 'message' in _get_response_data_as_dict(response).keys()
