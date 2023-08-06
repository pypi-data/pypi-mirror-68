from cpaassdk.utils import (
  outer_dict_value,
  process_response,
  id_from
)
from cpaassdk.resources.notification_channel import NotificationChannel

class Conversation:
  """
  CPaaS conversation.
  """
  def __init__(self, api):
    self.api = api
    self.types = {
      'SMS': 'sms'
    }

  @property
  def base_url(self):
    return '/cpaas/smsmessaging/v1/{}'.format(self.api.user_id)

  def create_message(self, params):
    """
      Send a new outbound message

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible value(s) - sms. Check conversation.types for more options.
        params['sender_address'] (:obj:`str`): Sender address information, basically the from address. E164 formatted DID number passed as a value, which is owned by the user. If the user wants to let CPaaS uses the default assigned DID number, this field can either has "default" value or the same value as the user_id.
        params['destination_address'] (:obj:`array[str]`): Indicates which DID number(s) used as destination for this SMS.
        params['message'] (:obj:`str`): SMS text message
    """
    message_type = params.get('type')
    destination_address = params.get('destination_address')
    address =  destination_address if type(destination_address) is list else [ destination_address ]
    if (message_type == self.types['SMS']):
      options = {
        'body': {
          'outboundSMSMessageRequest': {
            'address': address,
            'clientCorrelator': self.api.config.client_correlator,
            'outboundSMSTextMessage': {
              'message': params.get('message')
            }
          }
        }
      }

      url = '{}/outbound/{}/requests'.format(self.base_url, params.get('sender_address'))

      response = self.api.send_request(url, options, 'post')

      def custom_response(res):
        obj = res['outbound_sms_message_request']

        return {
          'message': obj['outbound_sms_text_message']['message'],
          'sender_address': obj['sender_address'],
          'delivery_info': obj['delivery_info_list']['delivery_info']
        }

      return process_response(response, callback=custom_response)

  def get_messages(self, params):
    """
      Gets all messages.

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible value(s) - sms. Check conversation.types for more options
        params['remote_address'] (:obj:`str`): Remote address information while retrieving the SMS history, basically the destination telephone number that user exchanged SMS before. E164 formatted DID number passed as a value.
        params['local_address'] (:obj:`str`): Local address information while retrieving the SMS history, basically the source telephone number that user exchanged SMS before.
        params['query'] (:obj:`dict`, optional): To hold all query related parameters.
        params['query']['name'] (:obj:`int`, optional): Performs search operation on first_name and last_name fields.
        params['query']['first_name'] (:obj:`int`, optional): Performs search for the first_name field of the directory items.
        params['query']['last_name'] (:obj:`int`, optional): Performs search for the last_name field of the directory items.
        params['query']['user_name'] (:obj:`int`, optional): Performs search for the user_name field of the directory items.
        params['query']['phone_number'] (:obj:`int`, optional): Performs search for the fields containing a phone number, like businessPhoneNumber, homePhoneNumber, mobile, pager, fax.
        params['query']['order'] (:obj:`int`, optional): Ordering the contact results based on the requested sortBy value, order query parameter should be accompanied by sortBy query parameter.
        params['query']['sort_by'] (:obj:`int`, optional): SortBy value is used to detect sorting the contact results based on which attribute. If order is not provided with that, ascending order is used.
        params['query']['max'] (:obj:`int`, optional): Maximum number of contact results that has been requested from CPaaS for this query.
        params['query']['next'] (:obj:`string`, optional): Pointer for the next chunk of contacts, should be gathered from the previous query results.

    """
    message_type = params.get('type')
    options = {}
    url = ''
    remote_address = params.get('remote_address')
    local_address = params.get('local_address')

    if (message_type == self.types['SMS']):
      options = {
        'query': params.get('query')
      }

      url = '{}/remoteAddresses'.format(self.base_url)

      if (remote_address):
        url = '{}/{}'.format(url, remote_address)
      if (local_address):
        url = '{}/localAddresses/{}'.format(url, local_address)

      response = self.api.send_request(url, options)

      def custom_response(res):
        def remove_resource_url(item):
          item.pop('resourceurl')
          return item

        return list(map(remove_resource_url, res['sms_thread_list']['sms_thread']))

      return process_response(response, callback=custom_response)

  def get_status(self, params):
    """
      Read a conversation message status

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj: `str`): Type of conversation. Possible value(s) - sms. Check conversation.types for more options
        params['remote_address'] (:obj:`str`): Remote address information while retrieving the SMS history, basically the destination telephone number that user exchanged SMS before. E164 formatted DID number passed as a value.
        params['local_address'] (:obj:`str`): Local address information while retrieving the SMS history, basically the source telephone number that user exchanged SMS before.
        params['message_id'] (:obj:`str`): Identification of the SMS message.
    """
    url = ''
    message_type = params.get('type')
    if (message_type == self.types['SMS']):
      url = '{}/remoteAddresses/{}/localAddresses/{}/messages/{}/status'.format(self.base_url, params.get('remote_address'), params.get('local_address'), params.get('message_id'))
      response = self.api.send_request(url, {})

      return process_response(response, callback=outer_dict_value)

  def get_messages_in_thread(self, params):
    """
      Read all messages in a thread

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible value(s) - sms. Check conversation.types for more options
        params['local_address'] (:obj:`str`): Local address information while retrieving the SMS history, basically the source telephone number that user exchanged SMS before.
        params['remote_address'] (:obj:`str`): Remote address information while retrieving the SMS history, basically the destination telephone number that user exchanged SMS before. E164 formatted DID number passed as a value.
        params['query'] (:obj:`dict`, optional): To hold all query related parameters.
        params['query']['max'] (:obj:`int`, optional): Number of messages that is requested from CPaaS.
        params['query']['next'] (:obj:`string`, optional): Pointer for the next page to retrieve for the messages, provided by CPaaS in previous GET response.
        params['query']['new'] (:obj:`string`, optional): Filters the messages or threads having messages that are not received by the user yet
        params['query']['last_message_time'] (:obj:`int`, optional): Filters the messages or threads having messages that are sent/received after provided Epoch time
    """
    message_type = params.get('type')
    options = {}
    url = ''
    if (message_type == self.types['SMS']):
      options = {
        'query': params.get('query')
      }
      url = '{}/remoteAddresses/{}/localAddresses/{}/messages'.format(self.base_url, params.get('remote_address'), params.get('local_address'))

      response = self.api.send_request(url, options)

      def custom_response(res):
        def remove_resource_url(item):
          item.pop('resourceurl')
          return item

        return list(map(remove_resource_url, res['sms_message_list']['sms_message']))

      return process_response(response, callback=custom_response)

  def delete_message(self, params):
    """
      Delete conversation message

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible value(s) - sms. Check conversation.types for more options
        params['remote_address'] (:obj:`str`): Remote address information while retrieving the SMS history, basically the destination telephone number that user exchanged SMS before. E164 formatted DID number passed as a value.
        params['local_address'] (:obj:`str`): Local address information while retrieving the SMS history, basically the source telephone number that user exchanged SMS before.
        params['message_id'] (:obj:`str`, optional): Identification of the SMS message. If messageId is not passed then the SMS thread is deleted with all messages.

    """
    message_type = params.get('type')
    if (message_type == self.types['SMS']):
      url = '{}/remoteAddresses/{}/localAddresses/{}'.format(self.base_url, params.get('remote_address'), params.get('local_address'))

      if params.get('message_id'):
        url = '{}/messages/{}'.format(url, params.get('message_id'))

      response = self.api.send_request(url, {}, 'delete')

      return process_response(response, callback=outer_dict_value)

  def get_subscriptions(self, params):
    """
      Read all active subscriptions.

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible value(s) - sms. Check conversation.types for more options

    """
    url = ''
    message_type = params.get('type')

    if (message_type == self.types['SMS']):
      url = '{}/inbound/subscriptions'.format(self.base_url)

      response = self.api.send_request(url, {})

      def custom_response(res):
        def pluck(item):
          return {
            'channel_id': item['callback_reference']['notifyurl'],
            'destination_address': item['destination_address'],
            'subscription_id': id_from(item['resourceurl'])
          }

        if ('subscription_list' in res) and ('subscription' in res['subscription_list']):
          return list(map(pluck, res['subscription_list']['subscription']))
        else:
          res

      return process_response(response, callback=custom_response)

  def get_subscription(self, params):
    """
      Read active subscription

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible value(s) - sms. Check conversation.types for more options
        params['subscription_id'] (:obj:`str`): Resource ID of the subscription

    """
    url = ''
    message_type = params.get('type')

    if (message_type == self.types['SMS']):
      url = '{}/inbound/subscriptions/{}'.format(self.base_url, params.get('subscription_id'))

      response = self.api.send_request(url, {})

      def custom_response(res):
        if 'subscription' in response:
          obj = response['subscription']

          return {
            'notify_url': obj['callback_reference']['notifyurl'],
            'destination_address': obj['destination_address'],
            'subscription_id': id_from(obj['resourceurl'])
          }
        else:
          return {}

      return process_response(response, callback=custom_response)

  def subscribe(self, params):
    """
      Create a new subscription.

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible value(s) - SMS. Check conversation.types for more options
        params['webhook_url'] (:obj:`str`): HTTPS URL that is present in your application server which is accessible from the public web where the notifications should be sent to. Note: Should be a POST endpoint.
        params['destination_address'] (:obj:`str`, optional): The address that incoming messages are received for this subscription. If does not exist, CPaaS uses the default assigned DID number to subscribe against. It is suggested to provide the intended E164 formatted DID number within this parameter.

    """
    message_type = params.get('type')

    if (message_type == self.types['SMS']):
      channel = NotificationChannel(self.api).create_channel(params)

      options = {
        'body': {
          'subscription': {
            'callbackReference': {
              'notifyURL': channel['channel_id']
            },
            'clientCorrelator': self.api.config.client_correlator,
            'destinationAddress': params.get('destination_address')
          }
        }
      }
      url = '{}/inbound/subscriptions'.format(self.base_url)

      response = self.api.send_request(url, options, 'post')

      def custom_response(res):
        return {
          'webhook_url': params['webhook_url'],
          'destination_address': res['subscription']['destination_address'],
          'subscription_id': id_from(res['subscription']['resourceurl'])
        }

      return process_response(response, callback=custom_response)

  def unsubscribe(self, params):
    """
      Unsubscription from conversation notification

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible value(s) - sms. Check conversation.types for more options
        params['subscription_id'] (:obj:`str`): Resource ID of the subscription

    """
    message_type = params.get('type')
    if (message_type == self.types['SMS']):
      url = '{}/inbound/subscriptions/{}'.format(self.base_url, params.get('subscription_id'))

      response = self.api.send_request(url, {}, 'delete')

      def custom_response(res):
        return {
          'subscription_id': params['subscription_id'],
          'success': True,
          'message': 'Unsubscribed from {} conversation notification'.format(params['type'])
        }

      return process_response(response, callback=custom_response)