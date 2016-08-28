from django.contrib import admin
from .models import User, Follower, Message

# Register your models here.
class FollowerInline(admin.StackedInline):
    model = Follower
    extra = 3


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [FollowerInline]
    list_display = ('question_text', 'pub_date') # replace def __str__()

admin.site.register(User, UserAdmin)
