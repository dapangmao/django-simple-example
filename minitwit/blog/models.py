from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')

    class Meta:
        unique_together = ('follower', 'followed')


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextField()
    pub_date = models.DateTimeField(auto_now_add=True)
