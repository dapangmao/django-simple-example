- Postgres side 
```sql
CREATE TABLE messages (
    title       text,
    body        text,
    tsv         tsvector
);

CREATE INDEX tsv_idx ON messages USING gin(tsv);

CREATE FUNCTION messages_trigger() RETURNS trigger AS $$
begin
  new.tsv :=
     setweight(to_tsvector('pg_catalog.english', coalesce(new.title,'')), 'A') ||
     setweight(to_tsvector('pg_catalog.english', coalesce(new.body,'')), 'D');
  return new;
end
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
    ON messages FOR EACH ROW EXECUTE PROCEDURE messages_trigger();
    
    
``` 
- Django side

``` python
from django.contrib.postgres.search import SearchVectorField

class Messages(models.Model):
    title = TextField()
    body = TextField()
    tsv = SearchVectorField()

from django.db.models import F
from django.contrib.postgres.search import SearchRank, SearchQuery

query = SearchQuery('pig')

Messages.objects.annotate(rank=SearchRank(F('tsv'), query)).order_by('-rank')
```
