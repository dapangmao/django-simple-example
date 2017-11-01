
- It could be simplified as a builder pattern
```python
import requests
import json

class FlashTranslator:

    def __init__(self):
        self.kr = "http://36kr.com/api/info-flow/newsflash_columns/newsflashes?per_page=10"
        self.baidu = "http://translate.baidu.com/v2transapi"
        self.key_words = set(['created_at', 'published_at', 'updated_at', 'title', 'description', 'id'])
        self._kr_src = None
        self.result = None

    @property
    def kr_src(self):
        if self._kr_src is None:
            r = requests.get(self.kr)
            res = r.json()['data']['items']
            self._kr_src = [ {k: v for k,  v in row.items() if k in key_words} for row in res]
        return self._kr_src

    def translate(self):
        query = ""
        for d in self.kr_src:
            current = d['title'] + '\n' + d['description'].replace('\n', '') + '\n'
            query += current

        post_data = {
            'from': 'zh',
            'to': 'en',
            'query': query
        }

        p = requests.post(self.baidu, post_data)
        res = p.json()
        return res['trans_result']['data']

    def combine(self):
        data = self.translate()
        i = 0
        new_data = []
        for each_dict in self.kr_src:
            current = each_dict.copy()
            if current['title'].strip() == data[i]['src'].strip():
                current['translated_title'] = data[i]['dst']
            if current['description'].replace('\n', '').strip() == data[i+1]['src'].strip():
                current['translated_description'] = data[i+1]['dst']
            new_data.append(current)
            i += 2
        self.result = new_data


a = FlashTranslator()
a.combine()
a.result

```
