from unittest.mock import Mock

from cpaassdk.utils import (
  build_error_response,
  outer_dict_value,
  remove_empty_from_dict,
  process_response,
  id_from
)
from tests.util import deep_equal

class Response:
  def __init__(self, status_code = 200, type = 'test'):
    self.status_code = status_code
    self.type = type

  def json(self):
    if self.type == 'test':
      return {
        '__for_test__': {
          'KeyOne': 'ValueOne'
        }
      }
    elif self.type == 'error':
      return {
        'requestError': {
          'serviceException': {
            'messageId': 'test-exception-id',
            'text': 'Attribute %1 specified in message part %2 is a duplicate',
            'variables': [
              'john',
              'userName'
            ]
          }
        }
      }
    else:
      return {
        'resourceURL': 'some/random/test/url/test-code-id'
      }

class TestUtil:
  def test_remove_empty_from_dict(self):
    input = {
      'key-1': 10,
      'key-2': 20,
      'key-3': None,
      'key-4': ''
    }

    expected_output = {
      'key-1': 10,
      'key-2': 20
    }

    output = remove_empty_from_dict(input)

    assert deep_equal(output, expected_output)

  def test_build_error_response_with_message_id(self):
    input = {
      'request_error': {
        'service_exception': {
          'message_id': 'test-exception-id',
          'text': 'Attribute %1 specified in message part %2 is a duplicate',
          'variables': [
            'john',
            'userName'
          ]
        }
      }
    }

    expected_output = {
      'name': 'service_exception',
      'exception_id': 'test-exception-id',
      'message': 'Attribute john specified in message part userName is a duplicate'
    }

    output = build_error_response(input)

    assert deep_equal(output, expected_output)

  def test_build_error_response_without_message_id(self):
    input = {
      'message': 'Some error message'
    }

    expected_output = {
      'name': 'request_error',
      'exception_id': 'unknown',
      'message': 'Some error message'
    }

    output = build_error_response(input)

    assert deep_equal(output, expected_output)

  def test_build_error_response_with_error_description(self):
    input = {
      'error': 'error',
      'error_description': 'Some error message'
    }

    expected_output = {
      'name': 'request_error',
      'exception_id': 'error',
      'message': 'Some error message'
    }

    output = build_error_response(input)

    assert deep_equal(output, expected_output)

  def test_outer_dict_value(self):
    input = {
      'parent': {
        'child': {
          'grandchild': {
            'value': 10
          }
        }
      }
    }

    expected_output = {
      'child': {
        'grandchild': {
          'value': 10
        }
      }
    }

    output = outer_dict_value(input)

    assert deep_equal(output, expected_output)

  def test_id_from(self):
    input = '/some/url/test-id'

    expected_output = 'test-id'

    output = id_from(input)

    assert expected_output == output

  def test_process_response_with_test_response(self):
    input = Response()

    expected_output = {
      '__for_test__': {
        'key_one': 'ValueOne'
      }
    }

    output = process_response(input)

    assert expected_output == output

  def test_process_response_with_error_response(self):
    input = Response(status_code = 401, type = 'error')

    expected_output = {
      'name': 'service_exception',
      'exception_id': 'test-exception-id',
      'message': 'Attribute john specified in message part userName is a duplicate'
    }

    output = process_response(input)

    assert expected_output == output

  def test_process_response_with_normal_response_without_callback(self):
    input = Response(type = 'success')

    expected_output = {
      'resourceurl': 'some/random/test/url/test-code-id'
    }

    output = process_response(input)

    assert expected_output == output

  def test_process_response_with_normal_response_with_callback(self):
    input = Response(type = 'success')

    callback_input = {
      'resourceurl': 'some/random/test/url/test-code-id'
    }

    func = Mock()

    output = process_response(input, callback=func)

    func.assert_called_with(callback_input)