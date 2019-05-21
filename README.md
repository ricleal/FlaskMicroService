# TODO:

- VueJS Frontend

# FlaskMicroService
Flask RestFULL API, mongodb, gunicorn, docker + VueJS Frontend

# Backend

## Install mongodb

`apt-get install mongo-db`

to make sure is installed:

```bash
$ mongo --version
MongoDB shell version v3.6.3
git version: 9586e557d54ef70f9ca4b43c26892cd55257e1a5
OpenSSL version: OpenSSL 1.1.0g  2 Nov 2017
allocator: tcmalloc
modules: none
build environment:
    distarch: x86_64
    target_arch: x86_64

```

## Virtual env

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements_dev.txt 

```

## Mongo DB

Make sure no other instance of mongo is running:
```
sudo service mongodb stop
```

Launch mongo as:
```
mongod --dbpath=./data/db --smallfiles
```

Load some initial data:
```
python db/load.py
```

## Tests

Make sure the tests pass:
```
pytest -vs
```

## Production

Install the requirements production.

```
pip install -r requirements_prod.txt 
```

Launch the flask service with gunicorn, e.g.:

```bash
gunicorn -w 2 --bind 0.0.0.0:8000 app.wsgi:app
```

### Docker

```bash
cd backend/

#
docker-compose up --build

# See containers running
docker ps

# Test it in the browser:
# http://localhost:8080/books

```

** Test with curl **

```bash
# Get all books
curl -X GET http://localhost:8080/books
# Get book 101
curl -X GET http://localhost:8080/books/101

# NOT WORKING! See https://gist.github.com/subfuzion/08c5d85437d5d4f00e58
# Create book
curl -H "Content-Type: application/json" -X POST http://localhost:8080/books \
--trace-ascii /dev/stdout \
-d @- << EOF
{"book": {
    "id": 10001,
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
}}
EOF

# 
```

# Front end

## Instalation

Assuming that nodejs is installed:

```
sudo npm install -g @vue/cli
```

Type:
```
$ vue --version
3.7.0
```
You should have something similar to this.

To create a new project
```
vue create flask-example
```

Select:
- Babel
- Router
- VueX
- Linter
- Unit Testing

All the rest default


