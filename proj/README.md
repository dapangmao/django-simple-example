1. http://stackoverflow.com/questions/10194975/how-to-dynamically-add-remove-periodic-tasks-to-celery-celerybeat



2. http://stackoverflow.com/questions/20116573/in-celery-3-1-making-django-periodic-task?rq=1
3. http://stackoverflow.com/questions/10660202/how-do-i-set-a-backend-for-django-celery-i-set-celery-result-backend-but-it-is


--- 

## How to replicate under Windows:

- Overall, there are three processes needed in Windows
- 1. python manage.py celeryd -E -l info
- 2. python manage.py celerycam
- 3. celery beat -A proj -l info
- the result will be wriiten to djcelery_taskstate


## It will be better on Linux:

- python manage.py celeryd -E -B --loglevel=info
