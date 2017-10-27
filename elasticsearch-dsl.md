1. Query and aggregation
```
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

client = Elasticsearch()

s = Search(using=client, index="my-index") \
    .filter("term", category="search") \
    .query("match", title="python")   \
    .query(~Q("match", description="beta"))

s.aggs.bucket('per_tag', 'terms', field='tags') \
    .metric('max_lines', 'max', field='lines')

response = s.execute()

for hit in response:
    print(hit.meta.score, hit.title)
```

1.1 Search with nested field
```
a = Article.search().query('term', title__raw="Hello world!")
r = a.execute()
for hit in r:
    print(hit.meta.score, hit.meta.id, hit.title, hit.tags)
```


2. Persistence 
```
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class Article(DocType):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Meta:
        index = 'blog'

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(** kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from

# create the mappings in elasticsearch
Article.init()

# create and save and article
article = Article(meta={'id': 42}, title='Hello world!', tags=['test'])
article.body = ''' looong text '''
article.published_from = datetime.now()
article.save()

article = Article.get(id=42)
print(article.is_published())

# Display cluster health
print(connections.get_connection().cluster.health())”
```

3. Delete
```
s = Search().query("match", title="python")
response = s.delete()
```

4. MultiMatch
```
from elasticsearch_dsl.query import MultiMatch, Match
# {"multi_match": {"query": "python django", "fields": ["title", "body"]}}
MultiMatch(query='python django', fields=['title', 'body'])

# {"match": {"title": {"query": "web framework", "type": "phrase"}}}
Match(title={"query": "web framework", "type": "phrase"})

from elasticsearch_dsl import MultiSearch, Search

ms = MultiSearch(index='blogs')

ms = ms.add(Search().filter('term', tags='python'))
ms = ms.add(Search().filter('term', tags='elasticsearch'))

responses = ms.execute()

for response in responses:
    print("Results for query %r." % response.search.query)
    for hit in response:
        print(hit.title)
```

5. Mapping
```
from elasticsearch_dsl import Keyword, Mapping, Nested, Text

# name your type
m = Mapping('my-type')

# add fields
m.field('title', 'text')

# you can use multi-fields easily
m.field('category', 'text', fields={'raw': Keyword()})

# you can also create a field manually
comment = Nested()
comment.field('author', Text())
comment.field('created_at', Date())

# and attach it to the mapping
m.field('comments', comment)

# you can also define mappings for the meta fields
m.meta('_all', enabled=False)

# save the mapping into index 'my-index'
m.save('my-index')

# get the mapping from our production cluster
m = Mapping.from_es('my-index', 'my-type', using='prod')

# update based on data in QA cluster
m.update_from_es('my-index', using='qa')

# update the mapping on production
m.save('my-index', using='prod')

class Post(DocType):
    class Meta:
        all = meta(enabled=False)
        routing = meta(required=True, path='post.author.id')
```

6. Django integration
```python

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date

connections.create_connection()

class BlogPostIndex(DocType):
    author = Text()
    posted_date = Date()
    title = Text()
    text = Text()

class BlogPost(models.Model):
   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost')
   posted_date = models.DateField(default=timezone.now)
   title = models.CharField(max_length=200)
   text = models.TextField(max_length=100
   
   def indexing(self):
       obj = BlogPostIndex(
          meta={'id': self.id},
          author=self.author.username,
          posted_date=self.posted_date,
          title=self.title,
          text=self.text
       )
       obj.save()
       return obj.to_dict(include_meta=True)


from .models import BlogPost
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=BlogPost)
def index_post(sender, instance, **kwargs):
    instance.indexing()
```

7. Custom analyzer
```python
from elasticsearch_dsl import Index, DocType, Text, analyzer

blogs = Index('blogs')

# define custom settings
blogs.settings(
    number_of_shards=1,
    number_of_replicas=0
)

# define aliases
blogs.aliases(
    old_blogs={}
)

# register a doc_type with the index
blogs.doc_type(Post)

# can also be used as class decorator when defining the DocType
@blogs.doc_type
class Post(DocType):
    title = Text()

# You can attach custom analyzers to the index

html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

blogs.analyzer(html_strip)

# delete the index, ignore if it doesn't exist
blogs.delete(ignore=404)

# create the index in elasticsearch
blogs.create()
```
