from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NotificationModel


@receiver(post_save, sender=NotificationModel)
def limit_user_notifications(sender, instance, created, **kwargs):
    if created:
        # пользоватеь, связанный с уведомлением
        user_id = instance.user_id

        # все уведомления
        notifications = user_id.notifications.count()

        # Удаляем более старые уведомления
        if notifications > 10:
            notifications_delete = user_id.notifications.all().order_by('timestamp')[:notifications - 10]
            for notifications in notifications_delete:
                notifications.delete()


