import pytest

from cpaassdk.config import Config

class TestApi:
  def test_init_with_no_params(self):
    with pytest.raises(Exception) as e:
        assert Config()
    assert str(e.value) == 'Missing base_url in config.'

  def test_init_with_only_base_url(self):
    config = {
      'base_url': 'https://test-base-url.com'
    }

    with pytest.raises(Exception) as e:
        assert Config(config)
    assert str(e.value) == 'Missing client_id, mandatory value.'

  def test_init_with_base_url_and_client_id(self):
    config = {
      'base_url': 'https://test-base-url.com',
      'client_id': 'test-client-id'
    }

    with pytest.raises(Exception) as e:
        assert Config(config)
    assert str(e.value) == 'Missing client_secret or email/password. Either one has to be present for authentication.'

  def test_init_with_account_credentials_no_password(self):
    config = {
      'base_url': 'https://test-base-url.com',
      'client_id': 'test-client-id',
      'email': 'test-email'
    }

    with pytest.raises(Exception) as e:
        assert Config(config)
    assert str(e.value) == 'Missing client_secret or email/password. Either one has to be present for authentication.'

  def test_init_with_account_credentials_no_email(self):
    config = {
      'base_url': 'https://test-base-url.com',
      'client_id': 'test-client-id',
      'password': 'test-password'
    }

    with pytest.raises(Exception) as e:
        assert Config(config)
    assert str(e.value) == 'Missing client_secret or email/password. Either one has to be present for authentication.'

  def test_init_with_project_credentials(self):
    config = {
      'base_url': 'https://test-base-url.com',
      'client_id': 'test-client-id',
      'client_secret': 'test-client-secret'
    }

    obj = Config(config)

    assert obj.client_id == config['client_id']
    assert obj.base_url == config['base_url']
    assert obj.client_secret == config['client_secret']
    assert obj.client_correlator == config['client_id'] + '-python'

  def test_init_with_account_credentials(self):
    config = {
      'client_id': 'test_client_id',
      'base_url': 'https://test-base-url.com',
      'email': 'test-email',
      'password': 'test-cpassword'
    }

    obj = Config(config)

    assert obj.client_id == config['client_id']
    assert obj.base_url == config['base_url']
    assert obj.email == config['email']
    assert obj.password == config['password']
    assert obj.client_correlator == config['client_id'] + '-python'
