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
# Build the image:
docker build --tag=flask_microservice .
# Make sure it's there
docker image ls
# Run it in foreground (use -d to run as detached - background): local port is 8080
docker run -p 8080:8000 flask_microservice
# Test it in the browser:
# http://localhost:8080/todos

```
