r'''
Pure Flask REST API 
'''

from flask import Flask, jsonify, request


app = Flask(__name__)

books = [
    {
        "id": 0,
        "title": "Test Book 1",
        "isbn": "9781234567897",
        "published_date": "2019-04-12",
        "authors": [
            "Rea Horne",
            "Cristiano Searle"
        ]
    },
    {
        "id": 1,
        "title": "Test Book 2",
        "isbn": "9781234562397",
        "published_date": "2018-03-12",
        "authors": [
            "Abbey Sullivan",
            "Paige Parry",
            "Tahir Frey",
        ]
    }
]


@app.route('/', methods=['GET'])
def get_all():
    return jsonify(books)


@app.route('/books', methods=['POST'])
def add_book():
    '''
    To test:
    curl -X POST -H "Content-Type: application/json" \
    -d '{"id": 123, "title": "Test Book from post"}' \
    http://127.0.0.1:5000/books
    '''
    data = request.get_json()
    books.append(data)
    return "", 204


@app.route('/books', methods=['PUT'])
def update_book():
    '''
    # To test:
    curl -X POST -H "Content-Type: application/json" \
    -d '{"id": 123, "title": "Test Book from post"}' \
    http://127.0.0.1:5000/books
    curl http://127.0.0.1:5000/

    curl -X PUT -H "Content-Type: application/json" \
    -d '{"id": 123, "title": "Test Book from PUT updated"}' \
    http://127.0.0.1:5000/books
    curl http://127.0.0.1:5000/

    '''
    data = request.get_json()
    [d.update(data) for d in books if d['id'] == data['id']]
    return "", 201


if __name__ == "__main__":
    app.run(debug=True)
