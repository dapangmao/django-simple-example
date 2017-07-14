- User based models

```python
class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')

    class Meta:
        unique_together = ('follower', 'followed')


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000)
    pub_date = models.DateTimeField(auto_now_add=True)
```

- 
