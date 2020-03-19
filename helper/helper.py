import itertools
from flask import jsonify


def flatten(list_of_Lists):
    """Flatten one level of nesting
        From https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    return list(set(itertools.chain.from_iterable(list_of_Lists)))


def make_response(response, code):
    print(jsonify(response), code)
    return jsonify(response), code
