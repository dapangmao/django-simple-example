from django.contrib import admin
from .models import User, Follower, Message


class MessageInline(admin.StackedInline):
    model = Message
    extra = 3  # it will be 6 entries each user


class UserAdmin(admin.ModelAdmin):
    fieldsets = [('User', {'fields': ['username']})]
    inlines = [MessageInline]
    list_display = ('username', 'email') # replace def __str__()

admin.site.register(User, UserAdmin)
