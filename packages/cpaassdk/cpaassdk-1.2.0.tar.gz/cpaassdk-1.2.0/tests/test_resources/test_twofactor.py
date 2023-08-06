import responses

from cpaassdk.resources.twofactor import Twofactor
from tests.util import decallmethods, deep_equal
from tests.mocker import mock


@decallmethods(responses.activate)
class TestTwofactor:
  def base_url(self, api):
    return '/cpaas/auth/v1/{}'.format(api.user_id)

  def client(self, api):
    return Twofactor(api)

  def test_send_code(self, api):
    client = Twofactor(api)
    params = {
      'destination_address': [ '345', '567' ],
      'method': 'email',
      'length': 6,
      'type': 'numeric',
      'expiry': 120,
      'message': 'test message {code}',
      'subject': 'test'
    }

    expected_body = {
      'code': {
        'address': [ '345', '567' ],
        'method': 'email',
        'format': {
          'length': 6,
          'type': 'numeric'
        },
        'expiry': 120,
        'subject': 'test',
        'message': 'test message {code}'
      }
    }

    url = '{}/codes'.format(self.base_url(api))

    mock(url, 'POST')

    response = client.send_code(params)

    assert response['__for_test__']['url'] == api.config.base_url + url
    assert deep_equal(response['__for_test__']['body'], expected_body)

  def test_verify_code(self, api):
    client = Twofactor(api)
    params = {
      'code_id': 'test-code-id',
      'verification_code': 'test-verification-code'
    }

    url = '{}/codes/{}/verify'.format(self.base_url(api), params.get('code_id'))
    mock(url, 'PUT')
    response = client.verify_code(params)
    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_resend_code(self, api):
    client = Twofactor(api)
    params = {
      'destination_address': [ '345', '567' ],
      'method': 'email',
      'length': 6,
      'type': 'numeric',
      'expiry': 120,
      'message': 'test message {code}',
      'subject': 'test'
    }

    expected_body = {
      'code': {
        'address': [ '345', '567' ],
        'method': 'email',
        'format': {
          'length': 6,
          'type': 'numeric'
        },
        'expiry': 120,
        'subject': 'test',
        'message': 'test message {code}'
      }
    }

    url = '{}/codes'.format(self.base_url(api))
    mock(url, 'POST')
    response = client.send_code(params)

    assert response['__for_test__']['url'] == api.config.base_url + url
    assert deep_equal(response['__for_test__']['body'], expected_body)

  def test_delete_code(self, api):
    client = Twofactor(api)
    params = {
      'code_id': 'test-code_id'
    }

    url = '{}/codes/{}'.format(self.base_url(api), params.get('code_id'))
    mock(url, 'PUT')
    response = client.delete_code(params)
    assert response['__for_test__']['url'] == api.config.base_url + url
