from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    pw_hash = models.CharField(max_length=100)


class Follower(models.Model):
    who_id = models.ForeignKey(User, on_delete=models.CASCADE)
    whom_id = models.IntegerField()


class Message(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000)
    pub_date = models.DateTimeField('date published')
