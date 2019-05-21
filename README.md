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

Launch mongo as:

```
mongod --dbpath=./data/db --smallfiles
```

Load some initial data:
```
python db/load.py
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

```
curl -X GET http://localhost:8000/books
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


