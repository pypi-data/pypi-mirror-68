import pytest
import responses

from cpaassdk.api import Api
from cpaassdk.config import Config
from tests.mocker import mock_token

@pytest.fixture
@responses.activate
def api():
  mock_token()

  config = Config({
    'client_id': 'test-client-id',
    'client_secret': 'test-client-secret',
    'base_url': 'https://oauth-cpaas.att.com'
  })

  return Api(config)
