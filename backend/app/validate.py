from jsonschema import validate
import os
import json
from flask import request, jsonify, abort
from jsonschema.exceptions import ValidationError


dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'schema.json')) \
        as json_file:
    schema = json.load(json_file)

# validate(instance={
#     "id": 2345,
#     "title": "Flex 4 in Action",
#     "isbn": "1935182420",
#     "pageCount": 600,
#     "publishedDate": "2010-11-15T00:00:00.000Z",
#     "thumbnailUrl": "https://s3.amazonaws.com/AKIAJC5RLADLUMVRPFDQ.book-thumb-images/ahmed2.jpg",
#     "longDescription": "Using Flex, you can create high-quality, effective, and interactive Rich Internet Applications (RIAs) quickly and easily. Flex removes the complexity barrier from RIA development by offering sophisticated tools and a straightforward programming language so you can focus on what you want to do instead of how to do it. And the new features added in Flex 4 give you an even wider range of options!    Flex 4 in Action is an easy-to-follow, hands-on Flex tutorial that goes beyond feature coverage and helps you put Flex to work in real day-to-day tasks. You'll quickly master the Flex API and learn to apply the techniques that make your Flex applications stand out from the crowd.    The expert authors of Flex 4 in Action have one goal-to help you get down to business with Flex. Fast. Flex 4 in Action filters out the noise and dives into the core topics you need every day. Using numerous easy-to-understand examples, Flex 4 in Action gives you a strong foundation that you can build on as the complexity of your projects increases.    Interesting themes, styles, and skins  It's in there.  Working with databases  You got it.  Interactive forms and validation  You bet.  Charting techniques to help you visualize data  Bam!  And you'll get full coverage of these great Flex 4 upgrades:  Next generation Spark components-New buttons, form inputs, navigation controls and other visual components replace the Flex 3 \"Halo\" versions. Spark components are easier to customize, which makes skinning and theme design much faster  A new \"network monitor\" allows you to see the data communications between a Flex application and a backend server, which helps when trying to debug applications that are communicating to another system/service  Numerous productivity boosting features that speed up the process of creating applications  A faster compiler to take your human-written source code and convert it into a machine-readable format  Built-in support for unit testing allows you to improve the quality of your software, and reduce the time spent in testing",
#     "status": "PUBLISH",
#     "authors": [
#             "Tariq Ahmed",
#             "Dan Orlando",
#             "John C. Bland II",
#             "Joel Hooks"
#     ],
#     "categories": [
#         "Internet"
#     ]
# }, schema=schema)


def validator_decorator(func):
    ''' Validator decorator to use in Flask '''
    def func_wrapper(*args, **kwargs):
        json_data = request.get_json(force=True)
        try:
            validate(instance=json_data['book'], schema=schema)
        except ValidationError:
            return abort(422)
        return func(*args, **kwargs)
    return func_wrapper
