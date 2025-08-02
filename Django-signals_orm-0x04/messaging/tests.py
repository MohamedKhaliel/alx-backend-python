from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTest(TestCase):
    def test_notification_created_on_message(self):
        sender = User.objects.create_user(username='alice', password='testpass')
        receiver = User.objects.create_user(username='bob', password='testpass')
        
        msg = Message.objects.create(sender=sender, receiver=receiver, content='Hello Bob!')

        notifications = Notification.objects.filter(user=receiver, message=msg)
        self.assertEqual(notifications.count(), 1)
