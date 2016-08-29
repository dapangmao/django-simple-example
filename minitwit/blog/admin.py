from django.contrib import admin
from .models import User, Follower, Message


class MessageInline(admin.StackedInline):
    model = Message
    extra = 3


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['username']}),
        ('Date information', {'fields': ['email'], 'classes': ['collapse']}),
    ]
    inlines = [MessageInline]
    # list_display = ('text', 'pub_date') # replace def __str__()

admin.site.register(User, UserAdmin)
