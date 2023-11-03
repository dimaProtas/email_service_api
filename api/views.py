import json
from django.shortcuts import render, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserModel, NotificationModel
from .serialyzers import UserSerializer, NotificationSerializer, ReadNotificationSerializer
from .utils import send_email


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationSerializer



class CreateNotificationView(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id', None)
            target_id = serializer.validated_data.get('target_id', None)
            key = serializer.validated_data['key']
            data = serializer.validated_data.get('data', {})

            # Проверяем наличие user_id и email
            if user_id is not None:
                user = UserModel.objects.get(user_id=user_id)
                notification = NotificationModel(user_id=user, target_id=target_id, key=key, data=data)

            else:
                email = serializer.validated_data.get('email', None)
                if email is not None:
                    try:
                        user = UserModel.objects.get(email=email)
                        notification = NotificationModel(user_id=user, target_id=target_id, key=key, data=data)
                    except UserModel.DoesNotExist:
                        user = UserModel(email=email)
                        user.save()
                    notification = NotificationModel(user_id=user, target_id=target_id, key=key, data=data)

            if key == 'registration':
                send_email(request, notification, user)
            elif key == 'new_message' or key == 'new_post':
                notification.save()
            elif key == 'new_login':
                notification.save()
                send_email(request, notification, user)

            return Response({'success': True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def read_notification(request):
    serializer = ReadNotificationSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        notification_id = serializer.validated_data['id']
        notification = get_object_or_404(NotificationModel, user_id=user_id, id=notification_id)
        if notification:
            notification.is_new = False
            notification.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        else:
            print('Здесь')
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
    else:
        print('Не здесь.')
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_notification(request):
    user_id = request.query_params.get('user_id', None)
    skip = int(request.query_params.get('skip', 0))
    limit = int(request.query_params.get('limit', 10))

    if user_id is not None:
        all_notifications = NotificationModel.objects.filter(user_id=user_id)
        total_notifications = all_notifications.count()

        # Получить все уведомления
        all_notifications = all_notifications[skip:skip + limit]
        serializer = NotificationSerializer(all_notifications, many=True)

        new_count = sum(1 for notification in all_notifications if notification.is_new)

        data = {
            "elements": total_notifications,
            "new": new_count,
            "request": {
                "user_id": user_id,
                "skip": skip,
                "limit": limit,
            },
            "list": serializer.data,
        }
        return Response({'success': True, "data": data}, status.HTTP_200_OK)
    else:
        return Response({'success': False, 'message': 'User ID is required.'}, status=400)
