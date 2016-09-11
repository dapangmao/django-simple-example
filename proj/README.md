1. http://stackoverflow.com/questions/10194975/how-to-dynamically-add-remove-periodic-tasks-to-celery-celerybeat

```
I assume you've already read the django section from the docs, but have you seen this example project?

It doesn't use the scheduler but if you add this to settings.py:

from __future__ import absolute_import

from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    # crontab(hour=0, minute=0, day_of_week='saturday')
    'schedule-name': {  # example: 'file-backup' 
        'task': 'some_django_app.tasks....',  # example: 'files.tasks.cleanup' 
        'schedule': crontab(...)
    },
}

# if you want to place the schedule file relative to your project or something:
CELERYBEAT_SCHEDULE_FILENAME = "some/path/and/filename"
Now for the commands, forget about manage.py, just type  celery directly:

-B enables celery beat as always.

-A specifies the name of the celery app. Note this line in the celery.py of the example project: app = Celery('proj')

celery -A proj worker -B -l info
'django-celery' is not required, install it ONLY if you need to manage the schedule from the admin, or if you want to store task results in the DB through django's ORM:

INSTALLED_APPS += ('djcelery',)

# store schedule in the DB:
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
```
