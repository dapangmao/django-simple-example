from django.contrib import admin
from .models import Follower, Message
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class MessageInline(admin.StackedInline):
    model = Message


class FollowerInline(admin.StackedInline):
    model = Follower

class MyUserAdmin(UserAdmin):
    inlines = [MessageInline, FollowerInline]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
