import json
import jwt
import requests

from datetime import datetime
from cpaassdk.utils import remove_empty_from_dict, process_response
from .__version__ import __version__


class Api:
  def __init__(self, config):
    self.config = config
    self.user_id = None
    self.access_token = None
    self.id_token = None
    self.access_token_parsed = None
    self.id_token_parsed = None

    self.auth_token()

  def send_request(self, path, options = {}, verb = 'get', with_token = True):
    url = "{}{}".format(self.config.base_url, path)
    query = options.get('query')
    headers = self.compose_headers(options.get('headers'), with_token)
    request_body = remove_empty_from_dict(options.get('body'))
    body = json.dumps(request_body) if headers.get('Content-Type') == 'application/json' else request_body

    if verb == 'get':
      response = requests.get(url, params=query, headers=headers)
    elif verb == 'post':
      response = requests.post(url, data=body, headers=headers)
    elif verb == 'put':
      response = requests.put(url, data=body, headers=headers)
    elif verb == 'patch':
      response = requests.patch(url, data=body, headers=headers)
    elif verb == 'delete':
      response = requests.delete(url, headers=headers)
    else:
      raise Exception('Invalid verb')
    return response

  def compose_headers(self, request_headers = {}, with_token = True):
    base_headers = {
      'Content-Type': 'application/json',
      'Accept': '*/*'
    }

    if request_headers: base_headers.update(request_headers)

    if with_token:
      auth_token = self.auth_token()

      auth_headers = {
        'Authorization': 'Bearer {}'.format(auth_token),
        'X-Cpaas-Agent': 'python-sdk/{}'.format(__version__)
      }

      base_headers.update(auth_headers)

    return base_headers

  def auth_token(self):
    if self.token_expired():
      auth_tokens = self.tokens()

      self.set_tokens(auth_tokens)

    return self.access_token

  def tokens(self):
    options = {
      'body': {
        'client_id': self.config.client_id,
        'scope': 'openid'
      },
      'headers': {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }

    if self.config.client_secret:
      options.get('body').update({
        'grant_type': 'client_credentials',
        'client_secret': self.config.client_secret
      })
    else:
      options.get('body').update({
        'grant_type': 'password',
        'username': self.config.email,
        'password': self.config.password
      })

    response = self.send_request('/cpaas/auth/v1/token', options, 'post', False)

    return process_response(response)

  def set_tokens(self, tokens = {}):
    if tokens is None or type(tokens) != dict or tokens.get('access_token') == None:
      self.user_id = None
      self.access_token = None
      self.id_token = None
      self.access_token_parsed = None
      self.id_token_parsed = None
    else:
      self.access_token = tokens.get('access_token')
      self.id_token = tokens.get('id_token')
      self.access_token_parsed = jwt.decode(self.access_token, verify=False)
      self.id_token_parsed = jwt.decode(self.id_token, verify=False)
      self.user_id = self.id_token_parsed.get('preferred_username')

  def token_expired(self):
    if not self.access_token: return True

    min_buffer = (self.access_token_parsed.get('exp') - self.access_token_parsed.get('iat'))/2
    expires_in = self.access_token_parsed.get('exp') - int(datetime.now().timestamp()) - min_buffer
    return expires_in < 0
