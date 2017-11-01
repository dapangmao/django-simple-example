
- The reference is https://medium.freecodecamp.org/elasticsearch-with-django-the-easy-way-909375bc16cb
- Model

```python
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from elasticsearch_dsl import DocType, Text, Date, Index, Keyword, MetaField
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])

blogpost = Index("blogpost-index")

blogpost.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@blogpost.doc_type
class BlogPostIndex(DocType):
    author = Text(analyzer="snowball", fields={"raw": Keyword()})
    pub_date = Date()
    title = Text(analyzer="snowball", fields={"raw": Keyword()})
    text = Text(analyzer="snowball", fields={"raw": Keyword()})

    class Meta:
        all = MetaField(enabled=False)


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost')
    pub_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=1000)

    def indexing(self):
        # The author should be with author's username
        current = BlogPostIndex(meta={'id': self.id}, author=self.author.username, pub_date=self.pub_date,
                                title=self.title,
                                text=self.text)
        current.save()
        return current.to_dict(include_meta=True)
```

- Signals

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BlogPost


@receiver(post_save, sender=BlogPost)
def index_post(sender, instance, **kwargs):
    instance.indexing()
```

- App config
```python
from django.apps import AppConfig


class EsappConfig(AppConfig):
    name = 'esapp'

    def ready(self):
        import esapp.signals
```
