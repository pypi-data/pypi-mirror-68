from .twofactor import Twofactor
from .conversation import Conversation
from .notification import Notification

mappings = {
  'twofactor': Twofactor,
  'conversation': Conversation,
  'notification': Notification
}
