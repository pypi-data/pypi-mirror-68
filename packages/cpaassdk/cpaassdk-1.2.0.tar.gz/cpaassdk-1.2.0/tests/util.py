import json
from inspect import getmembers, isfunction, ismethod

def decallmethods(decorator, prefix='test_'):
  """
    decorates all methods in class which begin with prefix test_ to prevent
    accidental external HTTP requests.
  """
  def dectheclass(cls):
    for name, method in getmembers(cls, predicate=lambda x: isfunction(x) or ismethod(x)):
      if name.startswith(prefix):
        setattr(cls, name, decorator(method))

    return cls
  return dectheclass

def deep_equal(obj1, obj2):
  obj1 = to_dict(obj1)
  obj2 = to_dict(obj2)
  if obj1 == obj2:
    return True
  else:
    return False

def to_json(obj):
  if type(obj) == str:
    return json.dumps(json.loads(obj), sort_keys=True)
  else:
    return json.dumps(obj, sort_keys=True)

def to_dict(obj):
  if type(obj) == str:
    return json.dumps(json.loads(obj), sort_keys=True)
  else:
    return json.dumps(dict(obj), sort_keys=True)
  
