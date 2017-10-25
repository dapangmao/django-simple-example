```python

import feedparser
import json


base_url = "http://blog.sasanalysis.com/feeds/posts/default?start-index="

res = []

for i in range(1, 162, 25):
    url = base_url + str(i)
    data = feedparser.parse(url).entries
    for d in data:
        current = {}
        current['title'] = d.title
        current['post'] = d.content[0].value
        current['published'] = d.updated
        res.append(current)
        
with open('data.txt', 'w') as outfile:
    json.dump(res, outfile)       

with open('test.html', 'w') as outfile:
    for x in res:
        print(x['post'], end="\n", file=outfile)
        
```
