import functools
import warnings
import base64
import re
from json import dumps, loads


class GraphQLError(Exception):
    def __init__(self, mutation, error):
        super().__init__(f'Mutation "{mutation}" failed with error: "{error}"')


def format_result(name, result):
    if 'errors' in result:
        raise GraphQLError(name, result['errors'])
    return format_json(result['data'][name])


def content_escape(content):
    return content.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')


def get_data_type(path):
    if re.match(r'(jpg|jpeg)$', path.lower()):
        return 'image/png'


def encode_image(path):
    data_type = get_data_type(path)
    with open(path, 'rb') as image_file:
        return f'data:{data_type};base64,' + \
            base64.b64encode(image_file.read()).decode('ascii')


def is_url(path):
    return re.match(r'^(http://|https://)', path.lower())


def format_json(result):
    if result is None:
        return result
    if isinstance(result, list):
        return [format_json(elem) for elem in result]
    if isinstance(result, dict):
        for key, value in result.items():
            if key in ['jsonInterface', 'jsonMetadata', 'jsonResponse']:
                if value == '' or value is None:
                    result[key] = dict()
                else:
                    result[key] = loads(value)
            else:
                result[key] = format_json(value)
        return result
    return result


def deprecate(msg, type=DeprecationWarning):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(msg, type, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator
