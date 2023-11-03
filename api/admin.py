from django.contrib import admin
from .models import UserModel, NotificationModel


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'email']
    list_display_links = ['user_id']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestamp', 'is_new', 'user_id', 'key', 'target_id', 'data']
    list_display_links = ['id']


admin.site.register(UserModel, UserAdmin)
admin.site.register(NotificationModel, NotificationAdmin)
