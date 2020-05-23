from django.contrib import admin
from users.models import Profile, CustomerUser


admin.site.register(Profile)
admin.site.register(CustomerUser)
