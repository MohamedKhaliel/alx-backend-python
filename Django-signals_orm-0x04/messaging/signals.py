from django.db.models.signals import post_save ,pre_save
from django.dispatch import receiver
from .models import Message, Notification ,MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    if instance.id:  # Only if updating existing message
        try:
            original = Message.objects.get(id=instance.id)
            if original.content != instance.content:
                # Log old content
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass
