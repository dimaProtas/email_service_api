from rest_framework import serializers
from .models import UserModel, NotificationModel


class NotificationSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    class Meta:
        model = NotificationModel
        fields = '__all__'


class ReadNotificationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user_id = serializers.CharField()

    class Meta:
        model = NotificationModel
        fields = ['id', 'user_id']


class UserSerializer(serializers.ModelSerializer):
    notifications = NotificationSerializer(many=True, read_only=True, source='notifications.all')

    class Meta:
        model = UserModel
        fields = '__all__'
