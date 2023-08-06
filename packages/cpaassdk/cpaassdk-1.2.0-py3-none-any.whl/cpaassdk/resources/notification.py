import humps

from cpaassdk.utils import (
  outer_dict_value,
  id_from,
  is_test_response,
  is_error_response
)
from cpaassdk.resources.notification_channel import NotificationChannel

class Notification:
  """
  CPaaS notification helper methods
  """
  def __init__(self, api):
    self.api = api
    self.types = {
      'outbound_sms_message_notification': 'outbound',
      'inbound_sms_message_notification': 'inbound',
      'sms_subscription_cancellation_notification': 'subscriptionCancel',
      'sms_event_notification': 'event'
    }

  def parse(self, notification):
    """
      Parse inbound sms notification received in webhook. It parses the notification and returns simplified version of the response.

      Args:
        params (dict): Single parameter to hold all options
        notification (:obj:`JSON`): JSON received in the subscription webhook.

    """
    parsed_notification = humps.decamelize(notification)
    top_level_notification_key = list(parsed_notification.keys())[0]
    if (top_level_notification_key=='sms_subscription_cancellation_notification'):
      return {
        'subscription_id': id_from(parsed_notification[top_level_notification_key]['link'][0]['href']),
        'notification_id': parsed_notification[top_level_notification_key]['id'],
        'notification_date_time': parsed_notification[top_level_notification_key]['date_time'],
        'type': self.types[top_level_notification_key]
      }
    elif (top_level_notification_key == 'outbound_sms_message_notification') or (top_level_notification_key == 'inbound_sms_message_notification'):
      outbound_sms_messages = parsed_notification[top_level_notification_key]
      inbound_sms_messages = parsed_notification[top_level_notification_key]
      notification_id = parsed_notification[top_level_notification_key]['id']
      notification_date_time = parsed_notification[top_level_notification_key]['date_time']
      return {
        **outbound_sms_messages,
        **inbound_sms_messages,
        'notification_id': notification_id,
        'notification_date_time': notification_date_time,
        'type': self.types[top_level_notification_key]
      }
    elif (top_level_notification_key == 'sms_event_notification'):
      event_description = parsed_notification[top_level_notification_key]['event_description']
      event_type = parsed_notification[top_level_notification_key]['event_type']
      event_links = parsed_notification[top_level_notification_key]['link']
      event_id = parsed_notification[top_level_notification_key]['id']
      event_date_time = parsed_notification[top_level_notification_key]['date_time']
      return {
        'notification_id': event_id,
        'notification_date_time': event_date_time,
        'message_id': id_from(event_links[0]['href']),
        'type': self.types[top_level_notification_key],
        'event_details': {
          'description': event_description,
          'type': event_type
        }
      }
    else:
      return parsed_notification[top_level_notification_key]