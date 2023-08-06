import responses

from cpaassdk.resources.notification_channel import NotificationChannel
from tests.util import decallmethods, deep_equal
from tests.mocker import mock

@decallmethods(responses.activate)
class TestConversation:
  def base_url(self, api):
    return '/cpaas/notificationchannel/v1/{}'.format(api.user_id)

  def test_create_message(self, api):
    notification_channel = NotificationChannel(api)
    webhook_url = 'webhook-url'
    url = '{}/channels'.format(self.base_url(api))

    params = {
      'webhook_url': webhook_url
    }

    expected_body = {
      'notificationChannel': {
        'channelData': {
          'x-webhookURL': webhook_url
        },
        'channelType': 'webhooks',
        'clientCorrelator': api.config.client_correlator
      }
    }

    mock(url, 'POST')

    response = notification_channel.create_channel(params)

    assert response['__for_test__']['url'] == api.config.base_url + url
    assert deep_equal(response['__for_test__']['body'], expected_body)
