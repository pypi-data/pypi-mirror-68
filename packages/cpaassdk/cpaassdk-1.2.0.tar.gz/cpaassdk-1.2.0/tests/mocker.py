from datetime import datetime
from urllib.parse import parse_qs
import json
import jwt
import responses

def mock(url, verb, body = None):
  base_url = 'https://oauth-cpaas.att.com'
  request_url = base_url + url

  def request_callback(request):
    resp_body = body

    if not resp_body:
      resp_body = {
        '__for_test__': {
          'url': request.url,
          'body': parse_qs(request.body) if request.headers['Content-Type'] == 'application/x-www-form-urlencoded' else request.body,
          'headers': dict(request.headers)
        }
      }

    return (200, request.headers, json.dumps(resp_body))

  responses.add_callback(verb, request_url, callback=request_callback)


def mock_token():
  access_token_payload = {
    'exp': int(datetime.now().timestamp()) + 6*60*60,
    'iat': int(datetime.now().timestamp()) - 2*60*60
  }

  id_token_payload = {
    'preferred_username': 'test-user'
  }

  secret = 'test-secret'

  access_token = jwt.encode(access_token_payload, secret, algorithm='HS256').decode('utf-8')
  id_token = jwt.encode(id_token_payload, secret, algorithm='HS256').decode('utf-8')

  body = {
    'access_token': access_token,
    'id_token': id_token
  }

  mock('/cpaas/auth/v1/token', 'POST', body)
