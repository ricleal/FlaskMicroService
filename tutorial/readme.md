# Tutorial

## Microservices using Python Flask

## Slides

To view the slides just open them on the browser.

## Examples

### Requirements:

* Python >= 3.6
* `pip` or `conda` (needs to read and install the `requirements.txt` file).
* A REST Client to test the API.
  * Google Chrome: "Tabbed Postman - REST Client"
  * Firefox: "RESTClient"
  * Or `curl` if you are brave

### Examples in the `api` folder

* `ex_0.py`
  * Flask serving simple HTML
* `ex_.1py`
  * Pure Flask simple REST API
* `ex_2.py`
  * Flask RESTFull: `flask_restful`
* `ex_3.py`
  * Validation: `jsonschema`
* `ex_4.py`
  * Flask RESTFull: `flask_restful` & Validation: `jsonschema`
* `ex_5.py`
  * Flask RESTFull Plus: `flask_restplus`
* `ex_6.py`
  * Flask RESTFull: `flask_restful` & Memoization: `cachetools`
* **TODO:** `ex_7.py`
  * Flask RESTFull with DB: `flask_restful` & ORM: `SQLAlchemy`
* **TODO:** `ex_8.py`
  * Flask RESTFull with GraphQL: `flask_restful`,  ORM: `SQLAlchemy` & GtaphQL `Graphene`

### Run the examples:


```sh
# create a virtual environment
virtualenv -p python3 venv

# Activate it
source venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# run an example
python -m api.ex_0

```
