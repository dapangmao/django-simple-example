#### The basic structure

- 3 instances

![demo](https://github.com/dapangmao/django-simple-example/blob/master/images/Note1_0(2).png?raw=true)



#### The components

- Django 
  - provide DB and UI spports for Celery
    - use DB as result backend -> `pip install django_celery_results`
    - use DB and Admin to schedule any async tasks -> `django_celery_beat`
      - how to pass arguments?
  - settings.py
  ```
  CELERY_BROKER_URL = 'redis://localhost:6379/0'
  CELERY_RESULT_BACKEND = 'django-db'

  CELERY_ACCEPT_CONTENT = ['application/json']
  CELERY_TASK_SERIALIZER = 'json'
  CELERY_RESULT_SERIALIZER = 'json'
  ```

- Celery 
  - needs to instantiate two instances 
    - beat: `celery -A test_async  beat -l info -S django`
    - worker: `celery -A test_async worker -l info`
