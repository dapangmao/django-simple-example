from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')

    class Meta:
        unique_together = ('follower', 'followed')


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextUploadingField()
    pub_date = models.DateTimeField(auto_now_add=True)
    tags = ArrayField(models.CharField(max_length=30), null=True)
