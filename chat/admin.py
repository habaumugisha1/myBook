from django.contrib import admin
from chat.models import Notification, Message


admin.site.register(Notification)
admin.site.register(Message)
