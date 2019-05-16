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