from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'text', 'pub_date']
