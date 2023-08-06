class Config:
  def __init__(self, config = {}):
    self.client_id = config.get('client_id')
    self.client_secret = config.get('client_secret')
    self.email = config.get('email')
    self.password = config.get('password')
    self.base_url = config.get('base_url')
    self.client_correlator = '{}-python'.format(config.get('client_id'))

    if self.base_url is None:
      raise Exception('Missing base_url in config.')

    if self.client_id is None:
      raise Exception('Missing client_id, mandatory value.')

    if self.client_secret is None and (self.email is None or self.password is None):
      raise Exception('Missing client_secret or email/password. Either one has to be present for authentication.')