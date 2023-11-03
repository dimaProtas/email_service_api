# from django.db import models
from django.utils import timezone
import random
import string
from djongo import models


def generate_id():
    characters = string.ascii_letters + string.digits
    user_id = ''.join(random.choice(characters) for _ in range(24))
    while UserModel.objects.filter(user_id=user_id).exists():
        user_id = ''.join(random.choice(characters) for _ in range(24))
    return user_id


class UserModel(models.Model):
    user_id = models.CharField(primary_key=True, max_length=24, unique=True, default=generate_id)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user_id


class NotificationModel(models.Model):
    CHOICES = (
        ('registration', 'registration'),
        ('new_message', 'new_message'),
        ('new_post', 'new_post'),
        ('new_login', 'new_login'),
    )
    timestamp = models.DateTimeField(default=timezone.now)
    is_new = models.BooleanField(default=True)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='notifications')
    key = models.CharField(max_length=20, choices=CHOICES)
    target_id = models.CharField(max_length=24, unique=True, default=generate_id)
    data = models.JSONField(blank=True, null=True)
