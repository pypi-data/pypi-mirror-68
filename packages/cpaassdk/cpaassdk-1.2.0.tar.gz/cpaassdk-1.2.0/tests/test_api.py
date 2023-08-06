import responses

from freezegun import freeze_time
from datetime import datetime, timedelta

from tests.mocker import mock, mock_token
from tests.util import decallmethods, deep_equal
from cpaassdk.api import Api
from cpaassdk.config import Config

@decallmethods(responses.activate)
class TestApi:
  def test_init(self, api):
    assert api.user_id == 'test-user'
    assert api.access_token != None
    assert api.id_token != None

  def test_send_request_without_token(self, api):
    url = '/test-path'

    options = {
      'body': {
        'param1': 'test-value1',
        'param2': 'test-value2'
      },
      'headers': {
        'header1': 'test-header1'
      }
    }

    mock(url, 'POST')

    response = api.send_request(url, options, 'post', False).json()

    assert deep_equal(response['__for_test__']['body'], options['body'])
    assert response['__for_test__']['url'] == api.config.base_url + url
    assert response['__for_test__']['headers']['Content-Type'] == 'application/json'
    assert response['__for_test__']['headers']['header1'] == 'test-header1'
    assert response['__for_test__']['headers'].get('Authorization') == None

  def test_send_request_with_token(self, api):
    url = '/test-path'

    options = {
      'body': {
        'param1': 'test-value1',
        'param2': 'test-value2'
      },
      'headers': {
        'header1': 'test-header1'
      }
    }

    mock('/test-path', 'POST')

    response = api.send_request('/test-path', options, 'post').json()

    assert deep_equal(response['__for_test__']['body'], options['body'])
    assert response['__for_test__']['url'] == api.config.base_url + url
    assert response['__for_test__']['headers']['Content-Type'] == 'application/json'
    assert response['__for_test__']['headers']['header1'] == 'test-header1'
    assert response['__for_test__']['headers'].get('Authorization') == 'Bearer ' + api.access_token

  def test_compose_headers_without_token(self, api):
    headers = api.compose_headers({}, False)
    assert headers['Content-Type'] == 'application/json'
    assert headers['Accept'] == '*/*'
    assert headers.get('Authorization') == None

    request_headers = {
      'header1': 'test-header1'
    }
    headers = api.compose_headers(request_headers, False)
    assert headers['Content-Type'] == 'application/json'
    assert headers['Accept'] == '*/*'
    assert headers['header1'] == 'test-header1'
    assert headers.get('Authorization') == None

  def test_compose_headers_with_token(self, api):
    headers = api.compose_headers()
    assert headers['Content-Type'] == 'application/json'
    assert headers['Accept'] == '*/*'
    assert headers['Authorization'] == 'Bearer ' + api.access_token

    request_headers = {
      'header1': 'test-header1'
    }

    headers = api.compose_headers(request_headers)
    assert headers['Content-Type'] == 'application/json'
    assert headers['Accept'] == '*/*'
    assert headers['header1'] == 'test-header1'
    assert headers['Authorization'] == 'Bearer ' + api.access_token

  def test_auth_token(self, api):
    token = api.auth_token()

    assert token != None
    assert token == api.access_token

  def test_tokens_with_project_credentials(self):
    base_url = 'https://oauth-cpaas.att.com'
    path = '/cpaas/auth/v1/token'
    client_id = 'test-client-id'
    client_secret = 'test-client-secret'

    mock(path, 'POST' )

    config = Config({
      'client_id': client_id,
      'client_secret': client_secret,
      'base_url': base_url
    })

    api = Api(config)
    response = api.tokens()

    assert response['__for_test__']['url'] == base_url + path
    assert response['__for_test__']['body']['client_id'][0] == client_id
    assert response['__for_test__']['body']['client_secret'][0] == client_secret
    assert response['__for_test__']['body']['grant_type'][0] == 'client_credentials'
    assert response['__for_test__']['body']['scope'][0] == 'openid'

  def test_tokens_with_user_credentials(self):
    base_url = 'https://oauth-cpaas.att.com'
    path = '/cpaas/auth/v1/token'
    client_id = 'test-client-id'
    client_secret = 'test-client-secret'
    email = 'test@user.com'
    password = 'test-password'

    mock(path, 'POST' )
    config = Config({
      'client_id': 'test-client-id',
      'email': email,
      'password': password,
      'base_url': base_url
    })

    api = Api(config)
    response = api.tokens()

    assert response['__for_test__']['url'] == base_url + path
    assert response['__for_test__']['body']['client_id'][0] == client_id
    assert response['__for_test__']['body']['username'][0] == email
    assert response['__for_test__']['body']['password'][0] == password
    assert response['__for_test__']['body']['grant_type'][0] == 'password'
    assert response['__for_test__']['body']['scope'][0] == 'openid'

  def test_set_token(self, api):
    tokens = {
      'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjcwMTAyNzJ9.y8wvKUizfATF_QH-9na4192eilSADghLlbeDB-hSVaU',
      'id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ0ZXN0LXVzZXIifQ.DT1AAa5laejotLDA-5QOajkrW-FmqWHACmJedbDfrOw'
    }

    api.set_tokens(tokens)
    assert api.user_id == 'test-user'
    assert api.access_token == tokens['access_token']
    assert api.id_token == tokens['id_token']
    assert type(api.access_token_parsed) == dict
    assert type(api.id_token_parsed) == dict

    api.set_tokens()
    assert api.user_id == None
    assert api.access_token == None
    assert api.id_token == None
    assert api.access_token_parsed == None
    assert api.id_token_parsed == None

  def test_token_expired_when_token_not_expired(self, api):
    assert api.token_expired() == False

  def test_token_expired_when_token_expired(self, api):
    future_date_time = (datetime.now() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

    with freeze_time(future_date_time):
      assert api.token_expired() == True
