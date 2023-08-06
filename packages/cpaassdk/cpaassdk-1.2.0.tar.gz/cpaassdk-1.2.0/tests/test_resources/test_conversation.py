import responses

from cpaassdk.resources.conversation import Conversation, NotificationChannel
from tests.util import decallmethods, deep_equal
from tests.mocker import mock

@decallmethods(responses.activate)
class TestConversation:
  def base_url(self, api):
    return '/cpaas/smsmessaging/v1/{}'.format(api.user_id)

  def notification_channel_base_url(self, api):
    return '/cpaas/notificationchannel/v1/{}'.format(api.user_id)

  def test_create_message(self, api):
    conversation = Conversation(api)
    sender_address = '123'
    url = '{}/outbound/{}/requests'.format(self.base_url(api), sender_address)
    params = {
      'type': 'sms',
      'sender_address': sender_address,
      'destination_address': [ '345', '567' ],
      'message': 'Test message'
    }

    expected_body = {
      'outboundSMSMessageRequest': {
        'address': [ '345', '567' ],
        'clientCorrelator': 'test-client-id-python',
        'outboundSMSTextMessage': {
          'message': 'Test message'
        }
      }
    }

    mock(url, 'POST')

    response = conversation.create_message(params)

    assert response['__for_test__']['url'] == api.config.base_url + url
    assert deep_equal(response['__for_test__']['body'], expected_body)

  def test_get_messages_with_no_params(self, api):
    conversation = Conversation(api)
    url = '{}/remoteAddresses'.format(self.base_url(api))

    params = {
      'type': 'sms'
    }

    mock(url, 'GET')

    response = conversation.get_messages(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_get_messages_with_remote_address(self, api):
    conversation = Conversation(api)
    remote_address = 'test-remote-address'
    url = '{}/remoteAddresses/{}'.format(self.base_url(api), remote_address)

    params = {
      'type': 'sms',
      'remote_address': remote_address
    }

    mock(url, 'GET')

    response = conversation.get_messages(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_get_messages_with_all_params(self, api):
    conversation = Conversation(api)
    remote_address = 'test-remote-address'
    local_address = 'test-local-address'
    url = '{}/remoteAddresses/{}/localAddresses/{}'.format(self.base_url(api), remote_address, local_address)

    params = {
      'type': 'sms',
      'local_address': local_address,
      'remote_address': remote_address
    }

    mock(url, 'GET')

    response = conversation.get_messages(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_delete_message(self, api):
    conversation = Conversation(api)
    remote_address = 'test-remote-address'
    local_address = 'test-local-address'
    url = '{}/remoteAddresses/{}/localAddresses/{}'.format(self.base_url(api), remote_address, local_address)
    params = {
      'type': 'sms',
      'remote_address': remote_address,
      'local_address': local_address
    }

    mock(url, 'DELETE')

    response = conversation.delete_message(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_delete_message_with_message_id(self, api):
    conversation = Conversation(api)
    remote_address = 'test-remote-address'
    local_address = 'test-local-address'
    message_id = 'test-message-id'
    url = '{}/remoteAddresses/{}/localAddresses/{}/messages/{}'.format(self.base_url(api), remote_address, local_address, message_id)
    params = {
      'type': 'sms',
      'remote_address': remote_address,
      'local_address': local_address,
      'message_id': message_id
    }

    mock(url, 'DELETE')

    response = conversation.delete_message(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_get_messages_in_thread(self, api):
    conversation = Conversation(api)
    remote_address = 'test-remote-address'
    local_address = 'test-local-address'
    url = '{}/remoteAddresses/{}/localAddresses/{}/messages?max=10&new=test'.format(self.base_url(api), remote_address, local_address)
    params = {
      'type': 'sms',
      'remote_address': remote_address,
      'local_address': local_address,
      'query': {
        'max': 10,
        'new': 'test'
      }
    }

    mock(url, 'GET')

    response = conversation.get_messages_in_thread(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_get_status(self, api):
    conversation = Conversation(api)
    remote_address = 'test-remote-address'
    local_address = 'test-local-address'
    message_id = 'test-message-id'
    url = '{}/remoteAddresses/{}/localAddresses/{}/messages/{}/status'.format(self.base_url(api), remote_address, local_address, message_id)
    params = {
      'type': 'sms',
      'remote_address': remote_address,
      'local_address': local_address,
      'message_id': message_id
    }

    mock(url, 'GET')

    response = conversation.get_status(params)
    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_get_subscriptions(self, api):
    conversation = Conversation(api)
    url = '{}/inbound/subscriptions'.format(self.base_url(api))

    mock(url, 'GET')

    params = {
      'type': 'sms'
    }

    response = conversation.get_subscriptions(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_get_subscription(self, api):
    conversation = Conversation(api)
    subscription_id = 'test-subscription-id'
    url = '{}/inbound/subscriptions/{}'.format(self.base_url(api), subscription_id)
    params = {
      'type': 'sms',
      'subscription_id': subscription_id
    }

    mock(url, 'GET')

    response = conversation.get_subscription(params)

    assert response['__for_test__']['url'] == api.config.base_url + url

  def test_subscribe(self, api):
    notification_channel_url = '{}/channels'.format(self.notification_channel_base_url(api))

    notification_channel_resp_body = {
      'notificationChannel': {
        'callbackURL': 'test-channel-id',
        'channelData': {
          'x-webhookURL': 'test-webhook-url'
        },
        'channelType': 'Webhooks',
        'clientCorrelator': 'test-client-correlator',
        'resourceURL': '/cpaas/notificationchannel/v1/e33c51d7-6585-4aee-88ae-005dfae1fd3b/channels/wh-72b43d88-4cc1-466e-a453-ecbea3733a2e'
      }
    }

    mock(notification_channel_url, 'POST', notification_channel_resp_body)

    conversation = Conversation(api)
    url = '{}/inbound/subscriptions'.format(self.base_url(api))
    params = {
      'type': 'sms',
      'webhook_url': 'test-webhook-url',
      'destination_address': '123123'
    }
    expected_body = {
      'subscription': {
        'callbackReference': {
          'notifyURL': 'test-channel-id'
        },
        'clientCorrelator': api.config.client_correlator,
        'destinationAddress': '123123'
      }
    }

    mock(url, 'POST')
    response = conversation.subscribe(params)

    assert response['__for_test__']['url'] == api.config.base_url + url
    assert deep_equal(response['__for_test__']['body'], expected_body)

  def test_unsubscribe(self, api):
    client = Conversation(api)
    subscription_id = 'test-subscription-id'
    url = '{}/inbound/subscriptions/{}'.format(self.base_url(api), subscription_id)
    params = {
      'type': 'sms',
      'subscription_id': subscription_id
    }

    mock(url, 'DELETE')

    response = client.unsubscribe(params)

    assert response['__for_test__']['url'] == api.config.base_url + url
