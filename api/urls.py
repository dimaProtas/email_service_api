from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, NotificationViewSet, CreateNotificationView, read_notification, list_notification
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="API mailing DRF",
        default_version='v1',
        description="Message sending service",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="dima_protasevich92@mail.ru"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', CreateNotificationView.as_view()),
    path('read/', read_notification),
    path('list/', list_notification),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
