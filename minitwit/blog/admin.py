from django.contrib import admin
from .models import Follower, Message
from django.contrib.auth.models import User


# class MessageInline(admin.StackedInline):
#     model = Message
#
# class FollowerInline(admin.StackedInline):
#     model = Follower
#
# class UserAdmin(admin.ModelAdmin):
#     fieldsets = [('User', {'fields': ['username']})]
#     inlines = [MessageInline,]
#     list_display = ('username', 'email') # replace def __str__()
#
# admin.site.register(UserAdmin)
