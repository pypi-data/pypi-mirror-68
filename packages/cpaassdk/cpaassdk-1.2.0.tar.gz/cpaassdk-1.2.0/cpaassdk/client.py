from types import ModuleType

from .api import Api
from .config import Config
from . import resources

class Client:
  """
    Configure the SDK with client_id and client_secret.

    Example::

        client = Client({
          'client_id': '<private project key>',
          'client_secret': '<private project secret>',
          'base_url': '<base url>'
        })

        # or

        client = Client({
          'client_id': '<account client ID>',
          'email': '<account email>',
          'password': '<account password>',
          'base_url': '<base url>'
        })

    Args:
      params (dict): Single parameter to hold all options
      params['client_id'] (:obj:`str`): 	Private project key / Account client ID. If Private project key is used then client_secret is mandatory. If account client ID is used then email and password are mandatory.
      params['client_secret'] (:obj:`str`, optional): Private project secret.
      params['email'] (:obj:`str`, optional): Account login email.
      params['password'] (:obj:`str`, optional): Account login password.
      params['base_url'] (:obj:`str`): url of the server to be used.
  """
  def __init__(self, credentials):
    config = Config(credentials)

    self.setup(config)

  def setup(self, config):
    api = Api(config)

    for namespace, Klass in resources.mappings.items():
      setattr(self, namespace, Klass(api))
