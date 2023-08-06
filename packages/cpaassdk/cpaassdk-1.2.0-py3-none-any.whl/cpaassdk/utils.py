import humps
import json
import re

def remove_empty_from_dict(d):
  if type(d) is dict:
    return dict((k, remove_empty_from_dict(v)) for k, v in d.items() if v and remove_empty_from_dict(v))
  elif type(d) is list:
    return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
  else:
    return d

def is_error_response(res):
  return res.status_code >= 400

def is_test_response(res):
  return '__for_test__' in res

def build_error_response(res):
  """
  Sample error response
  {
    "request_error": {
      "service_exception": {
        "message_id": "SVC0005",
        "text": "Attribute %1 specified in message part %2 is a duplicate",
        "variables": [
          "john",
          "userName"
        ]
      }
    }
  }
  """
  if res:
    error_obj = find_message_id_containing_obj(res, 'message_id')
    if error_obj:
      return {
        'name' : error_obj['name'],
        'exception_id': error_obj['message_id'],
        'message': re.sub(r"%[0-9]", '{}', error_obj['text']).format(*error_obj['variables'])
      }
    elif 'error_description' in res:
      return {
        'name': 'request_error',
        'exception_id': res['error'],
        'message': res['error_description']
      }
    else:
      return {
        'name': 'request_error',
        'exception_id': 'unknown',
        'message': res['message']
      }

def find_message_id_containing_obj(obj, key, parent_key=''):
  if key in obj:
    obj['name'] = parent_key
    return obj
  for k, v in obj.items():
      if isinstance(v,dict):
        item = find_message_id_containing_obj(v, key, k)
        if item is not None:
          return item

def outer_dict_value(res):
  """
  Get the value of the top most key of a dict.
  """
  return list(res.values())[0]

def process_response(res, callback = None):
  response = humps.decamelize(res.json())

  if is_test_response(response):
    return response
  elif is_error_response(res):
    return build_error_response(response)
  elif callback:
    return callback(response)

  return response

def id_from(url):
  chunks = url.split('/')

  return chunks[len(chunks) - 1]
