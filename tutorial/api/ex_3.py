r'''
Using jsonschema to show how to validate XML
'''

from jsonschema import validate
from jsonschema.exceptions import ValidationError


book_right = {
    "id": 0,
    "title": "Test Book 1",
    "isbn": "9781234567897",
    "published_date": "2010-03-09",
    "authors": [
        "Rea Horne",
        "Cristiano Searle"
    ]
}

book_wrong = {
    "id": 0,
    "isbn": "9781234567897",
    "published_date": "2010-03-09",
    "authors": [
        "Rea Horne",
        "Cristiano Searle"
    ]
}

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "required": [
        "id",
        "title",
    ],
    "properties": {
        "id": {
            "type": "integer"
        },
        "title": {
            "type": "string"
        },
        "isbn": {
            "type": "string"
        },
        "published_date": {
            "type": "string"
        },
        "authors": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
    },
    "additionalProperties": False
}

validate(instance=book_right, schema=schema)

try:
    validate(instance=book_wrong, schema=schema)
except ValidationError as e:
    print(str(e))
