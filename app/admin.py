from django.contrib import admin
from .models import UserFriend, UserScore

# Register your models here.

admin.site.register(UserFriend)
admin.site.register(UserScore)