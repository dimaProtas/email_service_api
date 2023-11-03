from django.core.mail import send_mail
from django.contrib import messages
import json


def send_email(request, notification, user):
    timestamp = notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    # user_data = {
    #     "user_id": user.user_id,
    #     "email": user.email
    # }

    notification_data = {
        "id": notification.id,
        "timestamp": timestamp,
        "is_new": notification.is_new,
        "user_id": user.user_id,
        "key": notification.key,
        "target_id": notification.target_id,
        "data": notification.data,
    }
    notification_json = json.dumps(notification_data, indent=4)
    mail = send_mail('Сервис сообщений', notification_json, None, [user.email], fail_silently=False, )
    if mail:
        messages.success(request, 'Письмо отправлено!')
    else:
        messages.error(request, 'Ошибка отправки!')