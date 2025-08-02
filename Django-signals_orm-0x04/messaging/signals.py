from django.db.models.signals import post_save,pre_save, post_delete
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

@receiver(post_delete, sender=Message)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete messages where user was sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete message histories created by this user
    MessageHistory.objects.filter(edited_by=instance).delete()

    # If you have a Notification model:
    # Notification.objects.filter(user=instance).delete()
