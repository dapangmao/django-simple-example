#### The basic structure

- 3 instances

![demo](https://github.com/dapangmao/django-simple-example/blob/master/images/Note1_0(2).png?raw=true)

- The docs at http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

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


#### Docker parent

- docs
  https://docs.docker.com/compose/django/


- docker-compose.yml

  ```ymal
  version: '3'

  services:

    db:
      image: postgres:latest

    redis:
      image: redis:3.2-alpine

    web:
      build:
        context: .
        dockerfile: dockerfile
      image: web_image
      command: python3 manage.py runserver 0.0.0.0:8000
      ports:
        - "8000:8000"
      depends_on:
        - db
        - redis


    celery_worker:
      image: web_image
      command:  celery -A test_async worker -l info
      depends_on:
        - web


    celery_beat:
      image: web_image
      command:  celery -A test_async  beat -l info -S django
      depends_on:
        - celery_worker
  ```
 - dockerfile/Dockfile

  ```
  FROM python:3-slim
  ENV PYTHONUNBUFFERED 1
  RUN mkdir /code
  WORKDIR /code
  ADD requirements.txt /code/
  RUN pip install -r requirements.txt
  ADD . /code/
  ```

- `settings.py` for Django
  - the names of the images are parsed
```
CELERY_BROKER_URL = 'redis://redis:6379/0'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```
