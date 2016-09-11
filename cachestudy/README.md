
- very easy to use redis cache http://niwinz.github.io/django-redis/latest/


```
127.0.0.1:6379> monitor
OK
1473636468.581556 [2 127.0.0.1:63518] "GET" ":1:50.50.PNG"
1473636475.190085 [2 127.0.0.1:63518] "GET" ":1:50.50.PNG"
1473636478.171220 [2 127.0.0.1:63518] "GET" ":1:50.50.PNG"
1473636492.893198 [2 127.0.0.1:63518] "GET" ":1:50.50.PNG"
1473636501.021602 [2 127.0.0.1:63518] "GET" ":1:50.50.PNG"
1473636505.592735 [2 127.0.0.1:63518] "GET" ":1:50.500.PNG"
1473636509.081319 [2 127.0.0.1:63518] "GET" ":1:50.500.PNG"
```


- no worry about the seralization of the objects

```
In[3]: from django.core.cache import cache
In[4]: cache.set('pig', {'df': 1})
In[5]: cache.get('pig')
Out[5]: {'df': 1}
```
