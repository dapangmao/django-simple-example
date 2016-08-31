from django.contrib import admin
from .models import User, Follower, Message


class MessageInline(admin.StackedInline):
    model = Message

class FollowerInline(admin.StackedInline):
    model = Follower

class UserAdmin(admin.ModelAdmin):
    fieldsets = [('User', {'fields': ['username']})]
    inlines = [MessageInline, FollowerInline]
    list_display = ('username', 'email') # replace def __str__()

admin.site.register(User, UserAdmin)
