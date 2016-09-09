from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    who = models.ForeignKey(User, on_delete=models.CASCADE)
    whom = models.IntegerField()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000)
    pub_date = models.DateTimeField(auto_now_add=True)
