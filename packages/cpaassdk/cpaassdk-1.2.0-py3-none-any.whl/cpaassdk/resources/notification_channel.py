from cpaassdk.utils import process_response

class NotificationChannel:
  def __init__(self, api):
    self.api = api
    self.types = {
      'SMS': 'sms'
    }

  @property
  def base_url(self):
    return '/cpaas/notificationchannel/v1/{}'.format(self.api.user_id)

  def channels(self, params):
    """
    Retrive the list of active notification channels.

    Args:

    Returns a json.
    """
    url = '{}/channels'.format(self.base_url)
    response = self.api.send_request(url)

  def channel(self, params):
    """
      Retrieve a list of active notification channels

      Args:
        params (dict): Single parameter to hold all options
        params['channed_id'] (:obj:`str`): The channelId provided by CPaaS after creation. 

      Return:
        Returns a json
    """
    url = '{}/channels/{}'.format(self.base_url, params.get('channel_id'))
    response = self.api.send_request(url)

  def create_channel(self, params):
    """
    Creates a new notification channel, webhook type.

    Args:
      params (dict): Single parameter to hold all options
      params['webhook_url'] (:obj:`str`): Type of conversation. Possible values - SMS. Check conversation.types for more options

    Returns:
      Returns a json.
    """
    url = '{}/channels'.format(self.base_url)
    options = {
      'body': {
        'notificationChannel': {
          'channelData': {
            'x-webhookURL': params.get('webhook_url')
          },
          'channelType': 'webhooks',
          'clientCorrelator': self.api.config.client_correlator
        }
      }
    }

    response = self.api.send_request(url, options, 'post')

    def custom_response(res):
      obj = res['notification_channel']

      return {
        'channel_id': obj['callbackurl'],
        'webhook_url': obj['channel_data']['x-webhookurl'],
        'channel_type': obj['channel_type']
      }

    return process_response(response, callback=custom_response)
