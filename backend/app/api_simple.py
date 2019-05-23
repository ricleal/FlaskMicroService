from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "Test Book 1",
        "isbn": "1234",
        "pageCount": 10,
        "publishedDate": "2017-08-01T00:00:00.000-0700",
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
    },
    {
        "id": 2,
        "title": "Test Book",
        "isbn": "5678",
        "pageCount": 20,
        "publishedDate": "2018-08-01T00:00:00.000-0700",
        "thumbnailUrl": "http://www.test.com/test.jpg",
        "longDescription": "",
        "status": "PUBLISH",
        "authors": [
            "Mohamed Doe"
        ],
        "categories": [
            "Test 1",
            "Test 3",
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
