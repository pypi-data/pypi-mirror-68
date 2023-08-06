from cpaassdk.utils import (
  id_from,
  is_test_response,
  process_response
)

class Twofactor:
  """
  CPaaS provides Authentication API where a two-factor authentication (2FA) flow can be implemented by using that.
  """
  def __init__(self, api):
    self.api = api

  @property
  def base_url(self):
    return '/cpaas/auth/v1/{}'.format(self.api.user_id)

  def send_code(self, params):
    """
      Create a new authentication code

      Args:
        params (dict): Single parameter to hold all options
        params['destination_address'] (:obj:`array[str]`): Destination address of the authentication code being sent. For sms type authentication codes, it should contain a E164 phone number. For e-mail type authentication codes, it should contain a valid e-mail address.
        params['message'] (:obj:`str`): Message text sent to the destination, containing the placeholder for the code within the text. CPaaS requires to have *{code}* string within the text in order to generate a code and inject into the text. For email type code, one usage is to have the *{code}* string located within the link in order to get a unique link.
        params['method'] (:obj:`str`, optional): Type of the authentication code delivery method, sms and email are supported types. Possible values: sms, email
        params['subject'] (:obj:`str`, optional): When the method is passed as email then subject becomes a mandatory field to pass. The value passed becomes the subject line of the 2FA code email that is sent out to the destinationAddress.
        params['expiry'] (:obj:`int`, optional): Lifetime duration of the code sent in seconds. This can contain values between 30 and 3600 seconds.
        params['length'] (:obj:`int`, optional): Length of the authentication code tha CPaaS should generate for this request. It can contain values between 4 and 10.
        params['type'] (:obj:`str`, optional): Type of the code that is generated. If not provided, default value is numeric. Possible values: numeric, alphanumeric, alphabetic

    """
    destination_address = params.get('destination_address')
    address =  destination_address if type(destination_address) is list else [ destination_address ]

    options = {
      'body': {
        'code': {
          'address': address,
          'method': params.get('method') or 'sms',
          'format': {
            'length': params.get('length') or 6,
            'type': params.get('type') or 'numeric'
          },
          'expiry': params.get('expiry') or 120,
          'subject': params.get('subject'),
          'message': params.get('message')
        }
      }
    }

    url = '{}/codes'.format(self.base_url)

    response = self.api.send_request(url, options, 'post')

    def custom_response(res):
      return {
        'code_id': id_from(res['code']['resourceurl'])
      }

    return process_response(response, callback=custom_response)

  def verify_code(self, params):
    """
      Verifying authentication code.

      Args:
        params (dict): Single parameter to hold all options
        params['code_id'] (:obj:`str`): ID of the authentication code.
        params['verification_code'] (:obj:`str`): Code that is being verified
    """
    destination_address = params.get('destination_address')
    address =  destination_address if type(destination_address) is list else [ destination_address ]

    options = {
      'body': {
        'code': {
          'verify': params.get('verification_code'),
        }
      }
    }

    url = '{}/codes/{}/verify'.format(self.base_url, params.get('code_id'))

    response = self.api.send_request(url, options, 'put')

    if (is_test_response(response.json())):
      return response.json()

    if (response.status_code == 204):
      custom_response = {
        'verified': True,
        'message': 'Success'
      }
    else:
      custom_response = {
        'verified': False,
        'message': 'Code invalid or expired'
      }

    return custom_response


  def resend_code(self, params):
    """
      Resending the authentication code via same code resource, invalidating the previously sent code.

      Args:
        params (dict): Single parameter to hold all options
        params['code_id'] (:obj:`str`): ID of the authentication code.
        params['destination_address'] (:obj:`array[str]`): Destination address of the authentication code being sent. For sms type authentication codes, it should contain a E164 phone number. For e-mail type authentication codes, it should contain a valid e-mail address.
        params['message'] (:obj:`str`): Message text sent to the destination, containing the placeholder for the code within the text. CPaaS requires to have *{code}* string within the text in order to generate a code and inject into the text. For email type code, one usage is to have the *{code}* string located within the link in order to get a unique link.
        params['method'] (:obj:`str`, optional): Type of the authentication code delivery method, sms and email are supported types. Possible values: sms, email
        params['subject'] (:obj:`str`, optional): When the method is passed as email then subject becomes a mandatory field to pass. The value passed becomes the subject line of the 2FA code email that is sent out to the destinationAddress.
        params['expiry'] (:obj:`int`, optional): Lifetime duration of the code sent in seconds. This can contain values between 30 and 3600 seconds.
        params['length'] (:obj:`int`, optional): Length of the authentication code tha CPaaS should generate for this request. It can contain values between 4 and 10.
        params['type'] (:obj:`str`, optional): Type of the code that is generated. If not provided, default value is numeric. Possible values: numeric, alphanumeric, alphabetic

    """
    destination_address = params.get('destination_address')
    address =  destination_address if type(destination_address) is list else [ destination_address ]

    options = {
      'body': {
        'code': {
          'address': address,
          'method': params.get('method') or 'sms',
          'format': {
            'length': params.get('length') or 6,
            'type': params.get('type') or 'numeric'
          },
          'expiry': params.get('expiry') or 120,
          'message': params.get('message'),
          'subject': params.get('subject')
        }
      }
    }

    url = '{}/codes/{}'.format(self.base_url, params.get('code_id'))

    response = self.api.send_request(url, options, 'put')

    def custom_response(res):
      return {
        'code_id': id_from(res['code']['resourceurl'])
      }

    return process_response(response, callback=custom_response)

  def delete_code(self, params):
    """
      Delete authentication code resource.

      Args:
        params (dict): Single parameter to hold all options
        params['code_id'] (:obj:`str`): ID of the authentication code.
    """

    url = '{}/codes/{}'.format(self.base_url, params.get('code_id'))

    response = self.api.send_request(url, {}, 'put')

    def custom_response(res):
      return {
        'code_id': params.get('code_id'),
        'success': True
      }

    return process_response(response, callback=custom_response)
