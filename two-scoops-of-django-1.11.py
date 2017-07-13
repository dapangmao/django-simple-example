# Chapter 1: Coding Style

"""chapter_01_example_01.py """

# Stdlib imports
from math import sqrt
from os.path import abspath

# Core Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Third-party app imports
from django_extensions.db.models import TimeStampedModel

# Imports from your apps
from splits.models import BananaSplit


"""chapter_01_example_02.py """

# cones/views.py
from django.views.generic import CreateView

# DON'T DO THIS!
# Hardcoding of the 'cones' package
# with implicit relative imports
from cones.models import WaffleCone
from cones.forms import WaffleConeForm
from core.views import FoodMixin

class WaffleConeCreateView(FoodMixin, CreateView):
model = WaffleCone
form_class = WaffleConeForm


"""chapter_01_example_03.py """

# cones/views.py
from django.views.generic import CreateView

# Relative imports of the 'cones' package
from .models import WaffleCone
from .forms import WaffleConeForm
from core.views import FoodMixin

class WaffleConeCreateView(FoodMixin, CreateView):
model = WaffleCone
form_class = WaffleConeForm


"""chapter_01_example_04.py """

from django import forms
from django.db import models


"""chapter_01_example_05.py """

# ANTI-PATTERN: Don't do this!
from django.forms import *
from django.db.models import *


"""chapter_01_example_06.py """

# ANTI-PATTERN: Don't do this!
from django.db.models import CharField
from django.forms import CharField


"""chapter_01_example_07.py """

from django.db.models import CharField as ModelCharField
from django.forms import CharField as FormCharField


"""chapter_01_example_08.py """

patterns = [
url(regex='^add/$',
view=views.add_topping,
name='add-topping'),
]


"""chapter_01_example_09.py """

patterns = [
url(regex='^add/$',
view=views.add_topping,
name='add_topping'),
]


# Chapter 2: The Optimal Django Environment Setup

"""chapter_02_example_01.txt """

$ source ~/.virtualenvs/twoscoops/bin/activate


"""chapter_02_example_02.txt """

$ workon twoscoops


# Chapter 3: How to Lay Out Django Projects

"""chapter_03_example_01.txt """

django-admin.py startproject mysite
cd mysite
django-admin.py startapp my_app


"""chapter_03_example_02.txt """

mysite/
├── manage.py
├── my_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
├── migrations
│   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
├── mysite/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py


"""chapter_03_example_03.txt """

<repository_root>/
├── <configuration_root>/
├── <django_project_root>/


"""chapter_03_example_04.txt """

icecreamratings_project
├── config/
│   ├── settings/
│   ├── __init__.py
│   ├── urls.py
│   └── wsgi.py
├── docs/
├── icecreamratings/
│   ├── media/  # Development only!
│   ├── products/
│   ├── profiles/
│   ├── ratings/
│   ├── static/
│   └── templates/
├── .gitignore
├── Makefile
├── README.rst
├── manage.py
└── requirements.txt


"""chapter_03_example_05.txt """

~/projects/icecreamratings_project/
~/.envs/icecreamratings/


"""chapter_03_example_06.txt """

c:\projects\icecreamratings_project\
c:\envs\icecreamratings\


"""chapter_03_example_07.txt """

~/.virtualenvs/icecreamratings/


"""chapter_03_example_08.txt """

$ pip freeze


"""chapter_03_example_09.txt """

$ pip freeze > requirements.txt


"""chapter_03_example_10.txt """

$ cookiecutter https://github.com/pydanny/cookiecutter-django

Cloning into 'cookiecutter-django'...
remote: Counting objects: 2358, done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 2358 (delta 4), reused 0 (delta 0), pack-reused 2346
Receiving objects: 100% (2358/2358), 461.95 KiB, done.
Resolving deltas: 100% (1346/1346), done.

project_name ('project_name')? icecreamratings
repo_name ('icecreamratings')? icecreamratings_project
author_name ('Your Name')? Daniel and Audrey Roy Greenfeld
email ('audreyr@gmail.com')? hello@twoscoopspress.com
description ('A short description of the project.')? A website
for rating ice cream flavors and brands.
domain_name ('example.com')? icecreamratings.audreyr.com
version ('0.1.0')? 0.1.0
timezone ('UTC')? America/Los_Angeles
now ('2017/04/02')? 2017/04/02
year ('2017')?
use_whitenoise ('n')?
github_username ('audreyr')? twoscoops
full_name ('Audrey Roy')? Daniel and Audrey Roy Greenfeld


# Chapter 4: Fundamentals of Django App Design

"""chapter_04_example_01.txt """

# Common modules
scoops/
├── __init__.py
├── admin.py
├── forms.py
├── management/
├── migrations/
├── models.py
├── templatetags/
├── tests/
├── urls.py
├── views.py


"""chapter_04_example_02.txt """

# uncommon modules
scoops/
├── api/
├── behaviors.py
├── constants.py
├── context_processors.py
├── decorators.py
├── db/
├── exceptions.py
├── fields.py
├── factories.py
├── helpers.py
├── managers.py
├── middleware.py
├── signals.py
├── utils.py
├── viewmixins.py


# Chapter 5: Settings and Requirements Files

"""chapter_05_example_01.txt """

settings/
├── __init__.py
├── base.py
├── local.py
├── staging.py
├── test.py
├── production.py


"""chapter_05_example_02.txt """

python manage.py shell --settings=twoscoops.settings.local


"""chapter_05_example_03.txt """

python manage.py runserver --settings=twoscoops.settings.local


"""chapter_05_example_04.py """

from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql_psycopg2',
'NAME': 'twoscoops',
'HOST': 'localhost',
}
}

INSTALLED_APPS += ['debug_toolbar', ]


"""chapter_05_example_05.txt """

python manage.py runserver --settings=twoscoops.settings.local


"""chapter_05_example_06.py """

# settings/local_pydanny.py
from .local import *

# Set short cache timeout
CACHE_TIMEOUT = 30


"""chapter_05_example_07.txt """

settings/
__init__.py
base.py
local_audreyr.py
local_pydanny.py
local.py
staging.py
test.py
production.py


"""chapter_05_example_08.txt """

export SOME_SECRET_KEY=1c3-cr3am-15-yummy
export AUDREY_FREEZER_KEY=y34h-r1ght-d0nt-t0uch-my-1c3-cr34m


"""chapter_05_example_09.txt """

> setx SOME_SECRET_KEY 1c3-cr3am-15-yummy


"""chapter_05_example_10.txt """

[Environment]::SetEnvironmentVariable('SOME_SECRET_KEY',
'1c3-cr3am-15-yummy', 'User')
[Environment]::SetEnvironmentVariable('AUDREY_FREEZER_KEY',
'y34h-r1ght-d0nt-t0uch-my-1c3-cr34m', 'User')


"""chapter_05_example_11.txt """

[Environment]::SetEnvironmentVariable('SOME_SECRET_KEY',
'1c3-cr3am-15-yummy', 'Machine')
[Environment]::SetEnvironmentVariable('AUDREY_FREEZER_KEY',
'y34h-r1ght-d0nt-t0uch-my-1c3-cr34m', 'Machine')


"""chapter_05_example_12.txt """

unset SOME_SECRET_KEY
unset AUDREY_FREEZER_KEY


"""chapter_05_example_13.txt """

[Environment]::UnsetEnvironmentVariable('SOME_SECRET_KEY', 'User')
[Environment]::UnsetEnvironmentVariable('AUDREY_FREEZER_KEY', 'User')


"""chapter_05_example_14.txt """

eb setenv SOME_SECRET_KEY=1c3-cr3am-15-yummy  # Elastic Beanstalk
heroku config:set SOME_SECRET_KEY=1c3-cr3am-15-yummy  # Heroku


"""chapter_05_example_15.py """

>>> import os
>>> os.environ['SOME_SECRET_KEY']
'1c3-cr3am-15-yummy'


"""chapter_05_example_16.py """

# Top of settings/production.py
import os
SOME_SECRET_KEY = os.environ['SOME_SECRET_KEY']


"""chapter_05_example_17.py """

# settings/base.py
import os

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
"""Get the environment variable or return exception."""
try:
return os.environ[var_name]
except KeyError:
error_msg = 'Set the {} environment variable'.format(var_name)
raise ImproperlyConfigured(error_msg)


"""chapter_05_example_18.py """

SOME_SECRET_KEY = get_env_variable('SOME_SECRET_KEY')


"""chapter_05_example_19.py """

django.core.exceptions.ImproperlyConfigured: Set the SOME_SECRET_KEY
environment variable.


"""chapter_05_example_20.json """

{
"FILENAME": "secrets.json",
"SECRET_KEY": "I've got a secret!",
"DATABASES_HOST": "127.0.0.1",
"PORT": "5432"
}


"""chapter_05_example_21.py """

# settings/base.py
import json

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

# JSON-based secrets module
with open('secrets.json') as f:
secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
'''Get the secret variable or return explicit exception.'''
try:
return secrets[setting]
except KeyError:
error_msg = 'Set the {0} environment variable'.format(setting)
raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret('SECRET_KEY')


"""chapter_05_example_22.txt """

requirements/
├── base.txt
├── local.txt
├── staging.txt
├── production.txt


"""chapter_05_example_23.txt """

Django==1.11.0
psycopg2==2.6.2
djangorestframework==3.4.0


"""chapter_05_example_24.txt """

-r base.txt # includes the base.txt requirements file

coverage==4.2
django-debug-toolbar==1.5


"""chapter_05_example_25.txt """

-r base.txt # includes the base.txt requirements file

coverage==4.2
django-jenkins==0.19.0


"""chapter_05_example_26.txt """

-r base.txt # includes the base.txt requirements file


"""chapter_05_example_27.txt """

pip install -r requirements/local.txt


"""chapter_05_example_28.txt """

pip install -r requirements/production.txt


"""chapter_05_example_29.py """

# settings/base.py

# Configuring MEDIA_ROOT
# DON’T DO THIS! Hardcoded to just one user's preferences
MEDIA_ROOT = '/Users/pydanny/twoscoops_project/media'

# Configuring STATIC_ROOT
# DON’T DO THIS! Hardcoded to just one user's preferences
STATIC_ROOT = '/Users/pydanny/twoscoops_project/collected_static'

# Configuring STATICFILES_DIRS
# DON’T DO THIS! Hardcoded to just one user's preferences
STATICFILES_DIRS = ['/Users/pydanny/twoscoops_project/static']

# Configuring TEMPLATES
# DON’T DO THIS! Hardcoded to just one user's preferences
TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
DIRS: ['/Users/pydanny/twoscoops_project/templates',]
},
]


"""chapter_05_example_30.py """

# At the top of settings/base.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'static_root'
STATICFILES_DIRS = [BASE_DIR / 'static']
TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [BASE_DIR / 'templates']
},
]


"""chapter_05_example_31.py """

# At the top of settings/base.py

from os.path import abspath, dirname, join

def root(*dirs):
base_dir = join(dirname(__file__), '..', '..')
return abspath(join(bas_dir, *dirs))


BASE_DIR = root()
MEDIA_ROOT = root('media')
STATIC_ROOT = root('static_root')
STATICFILES_DIRS = [root('static')]
TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [root('templates')],
},
]


# Chapter 6: Model Best Practices

"""chapter_06_example_01.py """

from django.db import models

class TimeStampedModel(models.Model):
"""
An abstract base class model that provides self-
updating ``created`` and ``modified`` fields.
"""
created = models.DateTimeField(auto_now_add=True)
modified = models.DateTimeField(auto_now=True)

class Meta:
abstract = True


"""chapter_06_example_02.py """

class Meta:
abstract = True


"""chapter_06_example_03.py """

# flavors/models.py
from django.db import models

from core.models import TimeStampedModel

class Flavor(TimeStampedModel):
title = models.CharField(max_length=200)


"""chapter_06_example_04.py """

from django.db import migrations, models

def add_cones(apps, schema_editor):
Scoop = apps.get_model('scoop', 'Scoop')
Cone = apps.get_model('cone', 'Cone')

for scoop in Scoop.objects.all():
Cone.objects.create(
scoop=scoop,
style='sugar'
)

class Migration(migrations.Migration):

initial = True

dependencies = [
('scoop', '0051_auto_20670724'),
]

operations = [
migrations.CreateModel(
name='Cone',
fields=[
('id', models.AutoField(auto_created=True, primary_key=True,
serialize=False, verbose_name='ID')),
('style', models.CharField(max_length=10),
choices=[('sugar', 'Sugar'), ('waffle', 'Waffle')]),
('scoop', models.OneToOneField(null=True, to='scoop.Scoop'
on_delete=django.db.models.deletion.SET_NULL, )),
],
),
# RunPython.noop does nothing but allows reverse migrations to occur
migrations.RunPython(add_cones, migrations.RunPython.noop)
]


"""chapter_06_example_05.py """

# orders/models.py
from django import models

class IceCreamOrder(models.Model):
FLAVOR_CHOCOLATE = 'ch'
FLAVOR_VANILLA = 'vn'
FLAVOR_STRAWBERRY = 'st'
FLAVOR_CHUNKY_MUNKY = 'cm'

FLAVOR_CHOICES = (
(FLAVOR_CHOCOLATE, 'Chocolate'),
(FLAVOR_VANILLA, 'Vanilla'),
(FLAVOR_STRAWBERRY, 'Strawberry'),
(FLAVOR_CHUNKY_MUNKY, 'Chunky Munky')
)

flavor = models.CharField(
max_length=2,
choices=FLAVOR_CHOICES
)


"""chapter_06_example_06.py """

>>> from orders.models import IceCreamOrder
>>> IceCreamOrder.objects.filter(flavor=IceCreamOrder.FLAVOR_CHOCOLATE)
[<icecreamorder: 35>, <icecreamorder: 42>, <icecreamorder: 49>]


"""chapter_06_example_07.py """

from django import models
from enum import Enum

class IceCreamOrder(models.Model):
class FLAVORS(Enum):
chocolate = ('ch', 'Chocolate')
vanilla = ('vn', 'Vanilla')
strawberry = ('st', 'Strawberry')
chunky_munky = ('cm', 'Chunky Munky')

@classmethod
def get_value(cls, member):
return cls[member].value[0]

flavor = models.CharField(
max_length=2,
choices=[x.value for x in FLAVORS]
)


"""chapter_06_example_08.py """

>>> from orders.models import IceCreamOrder
>>> chocolate = IceCreamOrder.FLAVORS.get_value('chocolate')
>>> IceCreamOrder.objects.filter(flavor=chocolate)
[<icecreamorder: 35>, <icecreamorder: 42>, <icecreamorder: 49>]


"""chapter_06_example_09.py """

from django.db import models
from django.utils import timezone

class PublishedManager(models.Manager):

use_for_related_fields = True

def published(self, **kwargs):
return self.filter(pub_date__lte=timezone.now(), **kwargs)

class FlavorReview(models.Model):
review = models.CharField(max_length=255)
pub_date = models.DateTimeField()

# add our custom model manager
objects = PublishedManager()


"""chapter_06_example_10.py """

>>> from reviews.models import FlavorReview
>>> FlavorReview.objects.count()
35
>>> FlavorReview.objects.published().count()
31


"""chapter_06_example_11.py """

>>> from reviews.models import FlavorReview
>>> FlavorReview.objects.filter().count()
35
>>> FlavorReview.published.filter().count()
31


# Chapter 7: Queries and the Database Layer

"""chapter_07_example_01.py """

from django.core.exceptions import ObjectDoesNotExist

from flavors.models import Flavor
from store.exceptions import OutOfStock

def list_flavor_line_item(sku):
try:
return Flavor.objects.get(sku=sku, quantity__gt=0)
except Flavor.DoesNotExist:
msg = 'We are out of {0}'.format(sku)
raise OutOfStock(msg)

def list_any_line_item(model, sku):
try:
return model.objects.get(sku=sku, quantity__gt=0)
except ObjectDoesNotExist:
msg = 'We are out of {0}'.format(sku)
raise OutOfStock(msg)


"""chapter_07_example_02.py """

from flavors.models import Flavor
from store.exceptions import OutOfStock, CorruptedDatabase

def list_flavor_line_item(sku):
try:
return Flavor.objects.get(sku=sku, quantity__gt=0)
except Flavor.DoesNotExist:
msg = 'We are out of {}'.format(sku)
raise OutOfStock(msg)
except Flavor.MultipleObjectsReturned:
msg = 'Multiple items have SKU {}. Please fix!'.format(sku)
raise CorruptedDatabase(msg)


"""chapter_07_example_03.py """

# Don't do this!
from django.models import Q

from promos.models import Promo

def fun_function(**kwargs):
"""Find working ice cream promo"""
# Too much query chaining makes code go off the screen or page. Not good.
return Promo.objects.active().filter(Q(name__startswith=name)|Q(description__icontains=name)).exclude(status='melted')


"""chapter_07_example_04.py """

# Do this!
from django.models import Q

from promos.models import Promo

def fun_function(**kwargs):
"""Find working ice cream promo"""
results = Promo.objects.active()
results = results.filter(
Q(name__startswith=name) |
Q(description__icontains=name)
)
results = results.exclude(status='melted')
results = results.select_related('flavors')
return results


"""chapter_07_example_05.py """

# Do this!
from django.models import Q

from promos.models import Promo

def fun_function(**kwargs):
"""Find working ice cream promo"""
qs = (Promo
.objects
.active()
.filter(
Q(name__startswith=name) |
Q(description__icontains=name)
)
.exclude(status='melted')
.select_related('flavors')
)
return qs


"""chapter_07_example_06.py """

def fun_function(**kwargs):
"""Find working ice cream promo"""
qs = (
Promo
.objects
.active()
# .filter(
#     Q(name__startswith=name) |
#     Q(description__icontains=name)
# )
# .exclude(status='melted')
# .select_related('flavors')
)
import pdb; pdb.set_trace()
return qs


"""chapter_07_example_07.py """

# Don't do this!
from models.customers import Customer

customers = []
for customer in Customer.objects.iterator():
if customer.scoops_ordered > customer.store_visits:
customers.append(customer)


"""chapter_07_example_08.py """

from django.db.models import F

from models.customers import Customer

customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))


"""chapter_07_example_09.sql """

SELECT * from customers_customer where scoops_ordered > store_visits


"""chapter_07_example_10.py """

# settings/base.py

DATABASES = {
'default': {
# ...
'ATOMIC_REQUESTS': True,
},
}


"""chapter_07_example_11.py """

# flavors/views.py

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Flavor

@transaction.non_atomic_requests
def posting_flavor_status(request, pk, status):
flavor = get_object_or_404(Flavor, pk=pk)

# This will execute in autocommit mode (Django's default).
flavor.latest_status_change_attempt = timezone.now()
flavor.save()

with transaction.atomic():
# This code executes inside a transaction.
flavor.status = status
flavor.latest_status_change_success = timezone.now()
flavor.save()
return HttpResponse('Hooray')

# If the transaction fails, return the appropriate status
return HttpResponse('Sadness', status_code=400)


# Chapter 8: Function- and Class-Based Views

"""chapter_08_example_01.py """

# Don't do this!
from django.conf.urls import url
from django.views.generic import DetailView

from tastings.models import Tasting

urlpatterns = [
url(r'^(?P<pk>\d+)/$',
DetailView.as_view(
model=Tasting,
template_name='tastings/detail.html'),
name='detail'),
url(r'^(?P<pk>\d+)/results/$',
DetailView.as_view(
model=Tasting,
template_name='tastings/results.html'),
name='results'),
]


"""chapter_08_example_02.py """

from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView

from .models import Tasting

class TasteListView(ListView):
model = Tasting

class TasteDetailView(DetailView):
model = Tasting

class TasteResultsView(TasteDetailView):
template_name = 'tastings/results.html'

class TasteUpdateView(UpdateView):
model = Tasting

def get_success_url(self):
return reverse('tastings:detail',
kwargs={'pk': self.object.pk})


"""chapter_08_example_03.py """

from django.conf.urls import url

from . import views

urlpatterns = [
url(
regex=r'^$',
view=views.TasteListView.as_view(),
name='list'
),
url(
regex=r'^(?P<pk>\d+)/$',
view=views.TasteDetailView.as_view(),
name='detail'
),
url(
regex=r'^(?P<pk>\d+)/results/$',
view=views.TasteResultsView.as_view(),
name='results'
),
url(
regex=r'^(?P<pk>\d+)/update/$',
view=views.TasteUpdateView.as_view(),
name='update'
)
]


"""chapter_08_example_04.py """

urlpatterns += [
url(r'^tastings/', include('tastings.urls', namespace='tastings')),
]


"""chapter_08_example_05.py """

# tastings/views.py snippet
class TasteUpdateView(UpdateView):
model = Tasting

def get_success_url(self):
return reverse('tastings:detail',
kwargs={'pk': self.object.pk})


"""chapter_08_example_06.html """

{% extends 'base.html' %}

{% block title %}Tastings{% endblock title %}

{% block content %}
<ul>
{% for taste in tastings %}
<li>
<a href="{% url 'tastings:detail' taste.pk %}">{{ taste.title }}</a>
<small>
(<a href="{% url 'tastings:update' taste.pk %}">update</a>)
</small>
</li>
{% endfor %}
</ul>
{% endblock content %}


"""chapter_08_example_07.py """

# urls.py at root of project
urlpatterns += [
url(r'^contact/', include('contactmonger.urls',
namespace='contactmonger')),
url(r'^report-problem/', include('contactapp.urls',
namespace='contactapp')),
]


"""chapter_08_example_08.html """

{% extends "base.html" %}
{% block title %}Contact{% endblock title %}
{% block content %}
<p>
<a href="{% url 'contactmonger:create' %}">Contact Us</a>
</p>
<p>
<a href="{% url 'contactapp:report' %}">Report a Problem</a>
</p>
{% endblock content %}


"""chapter_08_example_09.py """

# Django FBV as a function
HttpResponse = view(HttpRequest)

# Deciphered into basic math (remember functions from algebra?)
y = f(x)

# ... and then translated into a CBV example
HttpResponse = View.as_view()(HttpRequest)



"""chapter_08_example_10.py """

from django.http import HttpResponse
from django.views.generic import View

# The simplest FBV
def simplest_view(request):
# Business logic goes here
return HttpResponse('FBV')

# The simplest CBV
class SimplestView(View):
def get(self, request, *args, **kwargs):
# Business logic goes here
return HttpResponse('CBV')


"""chapter_08_example_11.py """

# Don't do this!
def ice_cream_store_display(request, store_id):
store = get_object_or_404(Store, id=store_id)
date = timezone.now()
return render(request, 'melted_ice_cream_report.html', locals())


"""chapter_08_example_12.py """

# Don't do this!
def ice_cream_store_display(request, store_id):
store = get_object_or_404(Store, id=store_id)
now = timezone.now()
return render(request, 'melted_ice_cream_report.html', locals())


"""chapter_08_example_13.py """

def ice_cream_store_display(request, store_id):
return render(
request,
'melted_ice_cream_report.html',
{
'store': get_object_or_404(Store, id=store_id),
'now': timezone.now()
}
)


# Chapter 9: Best Practices for Function-Based Views

"""chapter_09_example_01.py """

from django.core.exceptions import PermissionDenied

def check_sprinkle_rights(request):
if request.user.can_sprinkle or request.user.is_staff:
return request

# Return a HTTP 403 back to the user
raise PermissionDenied


"""chapter_09_example_02.py """

from django.core.exceptions import PermissionDenied

def check_sprinkles(request):
if request.user.can_sprinkle or request.user.is_staff:
# By adding this value here it means our display templates
#   can be more generic. We don't need to have
#   {% if request.user.can_sprinkle or request.user.is_staff %}
#   instead just using
#   {% if request.can_sprinkle %}
request.can_sprinkle = True
return request

# Return a HTTP 403 back to the user
raise PermissionDenied


"""chapter_09_example_03.py """

# sprinkles/views.py
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Sprinkle
from .utils import check_sprinkles

def sprinkle_list(request):
"""Standard list view"""

request = check_sprinkles(request)

return render(request,
"sprinkles/sprinkle_list.html",
{"sprinkles": Sprinkle.objects.all()})

def sprinkle_detail(request, pk):
"""Standard detail view"""

request = check_sprinkles(request)

sprinkle = get_object_or_404(Sprinkle, pk=pk)

return render(request, "sprinkles/sprinkle_detail.html",
{"sprinkle": sprinkle})

def sprinkle_preview(request):
"""Preview of new sprinkle, but without the
check_sprinkles function being used.
"""
sprinkle = Sprinkle.objects.all()
return render(request,
"sprinkles/sprinkle_preview.html",
{"sprinkle": sprinkle})


"""chapter_09_example_04.py """

from django.views.generic import DetailView

from .models import Sprinkle
from .utils import check_sprinkles

class SprinkleDetail(DetailView):
"""Standard detail view"""

model = Sprinkle

def dispatch(self, request, *args, **kwargs):
request = check_sprinkles(request)
return super(SprinkleDetail, self).dispatch(
request, *args, **kwargs)


"""chapter_09_example_05.py """

import functools

def decorator(view_func):
@functools.wraps(view_func)
def new_view_func(request, *args, **kwargs):
# You can modify the request (HttpRequest) object here.
response = view_func(request, *args, **kwargs)
# You can modify the response (HttpResponse) object here.
return response
return new_view_func


"""chapter_09_example_06.py """

# sprinkles/decorators.py
from functools import wraps

from . import utils

# based off the decorator template from the previous chapter
def check_sprinkles(view_func):
"""Check if a user can add sprinkles"""
@wraps(view_func)
def new_view_func(request, *args, **kwargs):
# Act on the request object with utils.can_sprinkle()
request = utils.can_sprinkle(request)

# Call the view function
response = view_func(request, *args, **kwargs)

# Return the HttpResponse object
return response
return new_view_func


"""chapter_09_example_07.py """

# sprinkles/views.py
from django.shortcuts import get_object_or_404, render

from .decorators import check_sprinkles
from .models import Sprinkle

# Attach the decorator to the view
@check_sprinkles
def sprinkle_detail(request, pk):
"""Standard detail view"""

sprinkle = get_object_or_404(Sprinkle, pk=pk)

return render(request, "sprinkles/sprinkle_detail.html",
{"sprinkle": sprinkle})


# Chapter 10: Best Practices for Class-Based Views

"""chapter_10_example_01.py """

from django.views.generic import TemplateView

class FreshFruitMixin:

def get_context_data(self, **kwargs):
context = super(FreshFruitMixin,
self).get_context_data(**kwargs)
context["has_fresh_fruit"] = True
return context

class FruityFlavorView(FreshFruitMixin, TemplateView):
template_name = "fruity_flavor.html"


"""chapter_10_example_02.py """

# flavors/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from .models import Flavor

class FlavorDetailView(LoginRequiredMixin, DetailView):
model = Flavor


"""chapter_10_example_03.py """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
model = Flavor
fields = ['title', 'slug', 'scoops_remaining']

def form_valid(self, form):
# Do custom logic here
return super(FlavorCreateView, self).form_valid(form)


"""chapter_10_example_04.py """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
model = Flavor

def form_invalid(self, form):
# Do custom logic here
return super(FlavorCreateView, self).form_invalid(form)


"""chapter_10_example_05.py """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.functional import cached_property
from django.views.generic import UpdateView, TemplateView

from .models import Flavor
from .tasks import update_user_who_favorited

class FavoriteMixin:

@cached_property
def likes_and_favorites(self):
"""Returns a dictionary of likes and favorites"""
likes = self.object.likes()
favorites = self.object.favorites()
return {
"likes": likes,
"favorites": favorites,
"favorites_count": favorites.count(),

}

class FlavorUpdateView(LoginRequiredMixin, FavoriteMixin, UpdateView):
model = Flavor
fields = ['title', 'slug', 'scoops_remaining']

def form_valid(self, form):
update_user_who_favorited(
instance=self.object,
favorites=self.likes_and_favorites['favorites']
)
return super(FlavorUpdateView, self).form_valid(form)

class FlavorDetailView(LoginRequiredMixin, FavoriteMixin, TemplateView):
model = Flavor


"""chapter_10_example_06.html """

{# flavors/base.html #}
{% extends "base.html" %}

{% block likes_and_favorites %}
<ul>
<li>Likes: {{ view.likes_and_favorites.likes }}</li>
<li>Favorites: {{ view.likes_and_favorites.favorites_count }}</li>
</ul>
{% endblock likes_and_favorites %}


"""chapter_10_example_07.py """

# flavors/models.py
from django.db import models
from django.urls import reverse

class Flavor(models.Model):

STATUS_0 = 0
STATUS_1 = 1
STATUS_CHOICES=(
(STATUS_0, 'zero'),
(STATUS_1 = 'one'),
)

title = models.CharField(max_length=255)
slug = models.SlugField(unique=True)
scoops_remaining = models.IntegerField(choices=STATUS_CHOICES,
default=STATUS_0)

def get_absolute_url(self):
return reverse("flavors:detail", kwargs={"slug": self.slug})


"""chapter_10_example_08.py """

# flavors/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
model = Flavor
fields = ['title', 'slug', 'scoops_remaining']

class FlavorUpdateView(LoginRequiredMixin, UpdateView):
model = Flavor
fields = ['title', 'slug', 'scoops_remaining']

class FlavorDetailView(DetailView):
model = Flavor


"""chapter_10_example_09.py """

# flavors/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Flavor

class FlavorActionMixin:

fields = ['title', 'slug', 'scoops_remaining']

@property
def success_msg(self):
return NotImplemented

def form_valid(self, form):
messages.info(self.request, self.success_msg)
return super(FlavorActionMixin, self).form_valid(form)

class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin,
CreateView):
model = Flavor
success_msg = "Flavor created!"

class FlavorUpdateView(LoginRequiredMixin, FlavorActionMixin,
UpdateView):
model = Flavor
success_msg = "Flavor updated!"

class FlavorDetailView(DetailView):
model = Flavor


"""chapter_10_example_10.html """

{% if messages %}
<ul class="messages">
{% for message in messages %}
<li id="message_{{ forloop.counter }}"
{% if message.tags %} class="{{ message.tags }}"
{% endif %}>
{{ message }}
</li>
{% endfor %}
</ul>
{% endif %}


"""chapter_10_example_11.py """

from django.views.generic import ListView

from .models import Flavor

class FlavorListView(ListView):
model = Flavor

def get_queryset(self):
# Fetch the queryset from the parent get_queryset
queryset = super(FlavorListView, self).get_queryset()

# Get the q GET parameter
q = self.request.GET.get("q")
if q:
# Return a filtered queryset
return queryset.filter(title__icontains=q)
# Return the base queryset
return queryset



"""chapter_10_example_12.html """

{# templates/flavors/_flavor_search.html #}
{% comment %}
Usage: {% include "flavors/_flavor_search.html" %}
{% endcomment %}
<form action="{% url "flavor_list" %}" method="GET">
<input type="text" name="q" />
<button type="submit">search</button>
</form>


"""chapter_10_example_13.py """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import FlavorForm
from .models import Flavor

class FlavorView(LoginRequiredMixin, View):

def get(self, request, *args, **kwargs):
# Handles display of the Flavor object
flavor = get_object_or_404(Flavor, slug=kwargs['slug'])
return render(request,
"flavors/flavor_detail.html",
{"flavor": flavor}
)

def post(self, request, *args, **kwargs):
# Handles updates of the Flavor object
flavor = get_object_or_404(Flavor, slug=kwargs['slug'])
form = FlavorForm(request.POST)
if form.is_valid():
form.save()
return redirect("flavors:detail", flavor.slug)


"""chapter_10_example_14.py """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Flavor
from .reports import make_flavor_pdf

class FlavorPDFView(LoginRequiredMixin, View):

def get(self, request, *args, **kwargs):
# Get the flavor
flavor = get_object_or_404(Flavor, slug=kwargs['slug'])

# create the response
response = HttpResponse(content_type='application/pdf')

# generate the PDF stream and attach to the response
response = make_flavor_pdf(response, flavor)

return response


# Chapter 11: Form Fundamentals

"""chapter_11_example_01.py """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
model = Flavor
fields = ['title', 'slug', 'scoops_remaining']

class FlavorUpdateView(LoginRequiredMixin, UpdateView):
model = Flavor
fields = ['title', 'slug', 'scoops_remaining']


"""chapter_11_example_02.py """

# core/validators.py
from django.core.exceptions import ValidationError

def validate_tasty(value):
"""Raise a ValidationError if the value doesn't start with the
word 'Tasty'.
"""
if not value.startswith('Tasty'):
msg = 'Must start with Tasty'
raise ValidationError(msg)


"""chapter_11_example_03.py """

# core/models.py
from django.db import models

from .validators import validate_tasty

class TastyTitleAbstractModel(models.Model):

title = models.CharField(max_length=255, validators=[validate_tasty])

class Meta:
abstract = True


"""chapter_11_example_04.py """

# flavors/models.py
from django.db import models
from django.urls import reverse

from core.models import TastyTitleAbstractModel

class Flavor(TastyTitleAbstractModel):
slug = models.SlugField()
scoops_remaining = models.IntegerField(default=0)

def get_absolute_url(self):
return reverse('flavors:detail', kwargs={'slug': self.slug})


"""chapter_11_example_05.py """

# flavors/forms.py
from django import forms

from .models import Flavor
from core.validators import validate_tasty

class FlavorForm(forms.ModelForm):
def __init__(self, *args, **kwargs):
super(FlavorForm, self).__init__(*args, **kwargs)
self.fields['title'].validators.append(validate_tasty)
self.fields['slug'].validators.append(validate_tasty)

class Meta:
model = Flavor


"""chapter_11_example_06.py """

# flavors/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Flavor
from .forms import FlavorForm

class FlavorActionMixin:

model = Flavor
fields = ['title', 'slug', 'scoops_remaining']

@property
def success_msg(self):
return NotImplemented

def form_valid(self, form):
messages.info(self.request, self.success_msg)
return super(FlavorActionMixin, self).form_valid(form)

class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin,
CreateView):
success_msg = 'created'
# Explicitly attach the FlavorForm class
form_class = FlavorForm

class FlavorUpdateView(LoginRequiredMixin, FlavorActionMixin,
UpdateView):
success_msg = 'updated'
# Explicitly attach the FlavorForm class
form_class = FlavorForm

class FlavorDetailView(DetailView):
model = Flavor


"""chapter_11_example_07.py """

# flavors/forms.py
from django import forms

from flavors.models import Flavor

class IceCreamOrderForm(forms.Form):
"""Normally done with forms.ModelForm. But we use forms.Form here
to demonstrate that these sorts of techniques work on every
type of form.
"""
slug = forms.ChoiceField(label='Flavor')
toppings = forms.CharField()

def __init__(self, *args, **kwargs):
super(IceCreamOrderForm, self).__init__(*args,
**kwargs)
# We dynamically set the choices here rather than
# in the flavor field definition. Setting them in
# the field definition means status updates won't
# be reflected in the form without server restarts.
self.fields['slug'].choices = [
(x.slug, x.title) for x in Flavor.objects.all()
]
# NOTE: We could filter by whether or not a flavor
#       has any scoops, but this is an example of
#       how to use clean_slug, not filter().

def clean_slug(self):
slug = self.cleaned_data['slug']
if Flavor.objects.get(slug=slug).scoops_remaining <= 0:
msg = 'Sorry, we are out of that flavor.'
raise forms.ValidationError(msg)
return slug


"""chapter_11_example_08.py """

# attach this code to the previous example (12.7)
def clean(self):
cleaned_data = super(IceCreamOrderForm, self).clean()
slug = cleaned_data.get('slug', '')
toppings = cleaned_data.get('toppings', '')

# Silly "too much chocolate" validation example
in_slug = 'chocolate' in slug.lower()
in_toppings = 'chocolate' in toppings.lower()
if in_slug and in_toppings:
msg = 'Your order has too much chocolate.'
raise forms.ValidationError(msg)
return cleaned_data


"""chapter_11_example_09.py """

# stores/models.py
from django.db import models
from django.urls import reverse

class IceCreamStore(models.Model):
title = models.CharField(max_length=100)
block_address = models.TextField()
phone = models.CharField(max_length=20, blank=True)
description = models.TextField(blank=True)

def get_absolute_url(self):
return reverse('store_detail', kwargs={'pk': self.pk})


"""chapter_11_example_10.py """

# stores/forms.py
from django import forms

from .models import IceCreamStore

class IceCreamStoreUpdateForm(forms.ModelForm):
# Don't do this! Duplication of the model field!
phone = forms.CharField(required=True)
# Don't do this! Duplication of the model field!
description = forms.TextField(required=True)

class Meta:
model = IceCreamStore


"""chapter_11_example_11.py """

# stores/forms.py
# Call phone and description from the self.fields dict-like object
from django import forms

from .models import IceCreamStore

class IceCreamStoreUpdateForm(forms.ModelForm):

class Meta:
model = IceCreamStore

def __init__(self, *args, **kwargs):
# Call the original __init__ method before assigning
# field overloads
super(IceCreamStoreUpdateForm, self).__init__(*args,
**kwargs)
self.fields['phone'].required = True
self.fields['description'].required = True


"""chapter_11_example_12.py """

# stores/forms.py
from django import forms

from .models import IceCreamStore

class IceCreamStoreCreateForm(forms.ModelForm):

class Meta:
model = IceCreamStore
fields = ['title', 'block_address', ]

class IceCreamStoreUpdateForm(IceCreamStoreCreateForm):

def __init__(self, *args, **kwargs):
super(IceCreamStoreUpdateForm,
self).__init__(*args, **kwargs)
self.fields['phone'].required = True
self.fields['description'].required = True

class Meta(IceCreamStoreCreateForm.Meta):
# show all the fields!
fields = ['title', 'block_address', 'phone',
'description', ]


"""chapter_11_example_13.py """

# stores/views
from django.views.generic import CreateView, UpdateView

from .forms import IceCreamStoreCreateForm, IceCreamStoreUpdateForm
from .models import IceCreamStore

class IceCreamCreateView(CreateView):
model = IceCreamStore
form_class = IceCreamStoreCreateForm

class IceCreamUpdateView(UpdateView):
model = IceCreamStore
form_class = IceCreamStoreUpdateForm


"""chapter_11_example_14.py """

# core/views.py
class TitleSearchMixin:

def get_queryset(self):
# Fetch the queryset from the parent's get_queryset
queryset = super(TitleSearchMixin, self).get_queryset()

# Get the q GET parameter
q = self.request.GET.get('q')
if q:
# return a filtered queryset
return queryset.filter(title__icontains=q)
# No q is specified so we return queryset
return queryset


"""chapter_11_example_15.py """

# add to flavors/views.py
from django.views.generic import ListView

from .models import Flavor
from core.views import TitleSearchMixin

class FlavorListView(TitleSearchMixin, ListView):
model = Flavor


"""chapter_11_example_16.py """

# add to stores/views.py
from django.views.generic import ListView

from .models import Store
from core.views import TitleSearchMixin

class IceCreamStoreListView(TitleSearchMixin, ListView):
model = Store


"""chapter_11_example_17.html """

{# form to go into stores/store_list.html template #}
<form action="" method="GET">
<input type="text" name="q" />
<button type="submit">search</button>
</form>


"""chapter_11_example_18.html """

{# form to go into flavors/flavor_list.html template #}
<form action="" method="GET">
<input type="text" name="q" />
<button type="submit">search</button>
</form>


# Chapter 12: Common Patterns for Forms

"""chapter_12_example_01.py """

import csv

from django.utils.six import StringIO

from .models import Purchase

def add_csv_purchases(rows):

rows = StringIO.StringIO(rows)
records_added = 0

# Generate a dict per row, with the first CSV row being the keys
for row in csv.DictReader(rows, delimiter=','):
# DON'T DO THIS: Tossing unvalidated data into your model.
Purchase.objects.create(**row)
records_added += 1
return records_added


"""chapter_12_example_02.py """

import csv

from django.utils.six import StringIO

from django import forms

from .models import Purchase, Seller

class PurchaseForm(forms.ModelForm):

class Meta:
model = Purchase

def clean_seller(self):
seller = self.cleaned_data['seller']
try:
Seller.objects.get(name=seller)
except Seller.DoesNotExist:
msg = '{0} does not exist in purchase #{1}.'.format(
seller,
self.cleaned_data['purchase_number']
)
raise forms.ValidationError(msg)
return seller

def add_csv_purchases(rows):

rows = StringIO.StringIO(rows)

records_added = 0
errors = []
# Generate a dict per row, with the first CSV row being the keys.
for row in csv.DictReader(rows, delimiter=','):

# Bind the row data to the PurchaseForm.
form = PurchaseForm(row)
# Check to see if the row data is valid.
if form.is_valid():
# Row data is valid so save the record.
form.save()
records_added += 1
else:
errors.append(form.errors)

return records_added, errors



"""chapter_12_example_03.html """

<form action="{% url 'flavor_add' %}" method="POST">


"""chapter_12_example_04.py """

from django import forms

from .models import Taster

class TasterForm(forms.ModelForm):

class Meta:
model = Taster

def __init__(self, *args, **kwargs):
# set the user as an attribute of the form
self.user = kwargs.pop('user')
super(TasterForm, self).__init__(*args, **kwargs)


"""chapter_12_example_05.py """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from .forms import TasterForm
from .models import Taster

class TasterUpdateView(LoginRequiredMixin, UpdateView):
model = Taster
form_class = TasterForm
success_url = '/someplace/'

def get_form_kwargs(self):
"""This method is what injects forms with keyword arguments."""
# grab the current set of form #kwargs
kwargs = super(TasterUpdateView, self).get_form_kwargs()
# Update the kwargs with the user_id
kwargs['user'] = self.request.user
return kwargs


"""chapter_12_example_06.py """

# core/models.py
from django.db import models

class ModelFormFailureHistory(models.Model):
form_data = models.TextField()
model_data = models.TextField()


"""chapter_12_example_07.py """

# flavors/views.py
import json

from django.contrib import messages
from django.core import serializers

from core.models import ModelFormFailureHistory

class FlavorActionMixin:

@property
def success_msg(self):
return NotImplemented

def form_valid(self, form):
messages.info(self.request, self.success_msg)
return super(FlavorActionMixin, self).form_valid(form)

def form_invalid(self, form):
"""Save invalid form and model data for later reference."""
form_data = json.dumps(form.cleaned_data)
# Serialize the form.instance
model_data = serializers.serialize('json', [form.instance])
# Strip away leading and ending bracket leaving only a dict
model_data = model_data[1:-1]
ModelFormFailureHistory.objects.create(
form_data=form_data,
model_data=model_data
)
return super(FlavorActionMixin,
self).form_invalid(form)



"""chapter_12_example_08.py """

from django import forms

class IceCreamReviewForm(forms.Form):
# Rest of tester form goes here
...

def clean(self):
cleaned_data = super(TasterForm, self).clean()
flavor = cleaned_data.get('flavor')
age = cleaned_data.get('age')

if flavor == 'coffee' and age < 3:
# Record errors that will be displayed later.
msg = 'Coffee Ice Cream is not for Babies.'
self.add_error('flavor', msg)
self.add_error('age', msg)

# Always return the full collection of cleaned data.
return cleaned_data


"""chapter_12_example_09.py """

# settings.py
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

INSTALLED_APPS = [
...
'django.forms',
...
]


"""chapter_12_example_10.py """

# flavors/widgets.py
from django.forms.widgets import TextInput

class IceCreamFlavorInput(TextInput):
"""Ice cream flavors must always end with 'Ice Cream'"""

def get_context(self, name, value, attrs):
context = super(IceCreamInput, self).get_context(name, value, attrs)
value = context['widget']['value']
if not value.strip().lower().endswith('ice cream'):
context['widget']['value'] = '{} Ice Cream'.format(value)
return context


# Chapter 13: Templates: Best Practices

"""chapter_13_example_01.txt """

templates/
├── base.html
├── ... (other sitewide templates in here)
├── freezers/
│   ├── ("freezers" app templates in here)


"""chapter_13_example_02.txt """

freezers/
├── templates/
│   ├── freezers/
│   │   ├── ... ("freezers" app templates in here)
templates/
├── base.html
├── ... (other sitewide templates in here)


"""chapter_13_example_03.txt """

templates/
├── base.html
├── dashboard.html # extends base.html
├── profiles/
│   ├── profile_detail.html # extends base.html
│   ├── profile_form.html # extends base.html


"""chapter_13_example_04.txt """

templates/
base.html
dashboard.html # extends base.html
profiles/
base_profiles.html # extends base.html
profile_detail.html # extends base_profiles.html
profile_form.html # extends base_profiles.html


"""chapter_13_example_05.py """

# vouchers/models.py
from django.db import models
from django.urls import reverse

from .managers import VoucherManager

class Voucher(models.Model):
"""Vouchers for free pints of ice cream."""
name = models.CharField(max_length=100)
email = models.EmailField()
address = models.TextField()
birth_date = models.DateField(blank=True)
sent = models.DateTimeField(null=True, default=None)
redeemed = models.DateTimeField(null=True, default=None)

objects = VoucherManager()


"""chapter_13_example_06.html """

{# templates/vouchers/ages.html #}
{% extends "base.html" %}

{% block content %}
<table>
<thead>
<tr>
<th>Age Bracket</th>
<th>Number of Vouchers Issued</th>
</tr>
</thead>
<tbody>
{% for age_bracket in age_brackets %}
<tr>
<td>{{ age_bracket.title }}</td>
<td>{{ age_bracket.count }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endblock content %}


"""chapter_13_example_07.py """

# vouchers/managers.py
from django.db import models
from django.utils import timezone

from dateutil.relativedelta import relativedelta

class VoucherManager(models.Manager):
def age_breakdown(self):
"""Returns a dict of age brackets/counts."""
age_brackets = []
now = timezone.now()

delta = now - relativedelta(years=18)
count = self.model.objects.filter(birth_date__gt=delta).count()
age_brackets.append(
{'title': '0-17', 'count': count}
)
count = self.model.objects.filter(birth_date__lte=delta).count()
age_brackets.append(
{'title': '18+', 'count': count}
)
return age_brackets


"""chapter_13_example_08.html """

<h2>Greenfelds Who Want Ice Cream</h2>
<ul>
{% for voucher in voucher_list %}
{# Don't do this: conditional filtering in templates #}
{% if 'greenfeld' in voucher.name.lower %}
<li>{{ voucher.name }}</li>
{% endif %}
{% endfor %}
</ul>

<h2>Roys Who Want Ice Cream</h2>
<ul>
{% for voucher in voucher_list %}
{# Don't do this: conditional filtering in templates #}
{% if 'roy' in voucher.name.lower %}
<li>{{ voucher.name }}</li>
{% endif %}
{% endfor %}
</ul>


"""chapter_13_example_09.py """

# vouchers/views.py
from django.views.generic import TemplateView

from .models import Voucher

class GreenfeldRoyView(TemplateView):
template_name = 'vouchers/views_conditional.html'

def get_context_data(self, **kwargs):
context = super(GreenfeldRoyView, self).get_context_data(**kwargs)
context['greenfelds'] = \
Voucher.objects.filter(name__icontains='greenfeld')
context['roys'] = Voucher.objects.filter(name__icontains='roy')
return context


"""chapter_13_example_10.html """

<h2>Greenfelds Who Want Ice Cream</h2>
<ul>
{% for voucher in greenfelds %}
<li>{{ voucher.name }}</li>
{% endfor %}
</ul>

<h2>Roys Who Want Ice Cream</h2>
<ul>
{% for voucher in roys %}
<li>{{ voucher.name }}</li>
{% endfor %}
</ul>


"""chapter_13_example_11.html """

{# list generated via User.object.all() #}
<h1>Ice Cream Fans and their favorite flavors.</h1>
<ul>
{% for user in user_list %}
<li>
{{ user.name }}:
{# DON'T DO THIS: Generated implicit query per user #}
{{ user.flavor.title }}
{# DON'T DO THIS: Second implicit query per user!!! #}
{{ user.flavor.scoops_remaining }}
</li>
{% endfor %}
</ul>


"""chapter_13_example_12.html """

{% comment %}
List generated via User.object.all().select_related('flavors')
{% endcomment %}
<h1>Ice Cream Fans and their favorite flavors.</h1>
<ul>
{% for user in user_list %}
<li>
{{ user.name }}:
{{ user.flavor.title }}
{{ user.flavor.scoops_remaining }}
</li>
{% endfor %}
</ul>


"""chapter_13_example_13.html """

{% comment %}Don't do this! This code bunches everything
together to generate pretty HTML.
{% endcomment %}
{% if list_type=='unordered' %}<ul>{% else %}<ol>{% endif %}{% for
syrup in syrup_list %}<li class="{{ syrup.temperature_type|roomtemp
}}"><a href="{% url 'syrup_detail' syrup.slug %}">{% syrup.title %}
</a></li>{% endfor %}{% if list_type=='unordered' %}</ul>{% else %}
</ol>{% endif %}


"""chapter_13_example_14.html """

{# Use indentation/comments to ensure code quality #}
{# start of list elements #}
{% if list_type=='unordered' %}
<ul>
{% else %}
<ol>
{% endif %}

{% for syrup in syrup_list %}
<li class="{{ syrup.temperature_type|roomtemp }}">
<a href="{% url 'syrup_detail' syrup.slug %}">
{% syrup.title %}
</a>
</li>
{% endfor %}
{# end of list elements #}
{% if list_type=='unordered' %}
</ul>
{% else %}
</ol>
{% endif %}


"""chapter_13_example_15.html """

{# simple base.html #}
{% load staticfiles %}
<html>
<head>
<title>
{% block title %}Two Scoops of Django{% endblock title %}
</title>
{% block stylesheets %}
<link rel="stylesheet" type="text/css"
href="{% static 'css/project.css' %}">
{% endblock stylesheets %}
</head>
<body>
<div class="content">
{% block content %}
<h1>Two Scoops</h1>
{% endblock content %}
</div>
</body>
</html>


"""chapter_13_example_16.html """

{% extends "base.html" %}
{% load staticfiles %}
{% block title %}About Audrey and Daniel{% endblock title %}
{% block stylesheets %}
{{ block.super }}
<link rel="stylesheet" type="text/css"
href="{% static 'css/about.css' %}">
{% endblock stylesheets %}
{% block content %}
{{ block.super }}
<h2>About Audrey and Daniel</h2>
<p>They enjoy eating ice cream</p>
{% endblock content %}


"""chapter_13_example_17.html """

<html>
<head>
<title>
About Audrey and Daniel
</title>
<link rel="stylesheet" type="text/css"
href="/static/css/project.css">
<link rel="stylesheet" type="text/css"
href="/static/css/about.css">
</head>
<body>
<div class="content">
<h1>Two Scoops</h1>
<h2>About Audrey and Daniel</h2>
<p>They enjoy eating ice cream</p>
</div>
</body>
</html>


"""chapter_13_example_18.html """

{% extends "base.html" %}
{% block stylesheets %}
{{ block.super }} {# this brings in project.css #}
<link rel="stylesheet" type="text/css"
href="{% static 'css/custom.css' %}" />
{% endblock stylesheets %}


"""chapter_13_example_19.html """

{% extends "base.html" %}
{% block stylesheets %}
<link rel="stylesheet" type="text/css"
href="{% static 'css/dashboard.css' %}" />
{% comment %}
By not using {{ block.super }}, this block overrides the
stylesheet block of base.html
{% endcomment %}
{% endblock stylesheets %}


"""chapter_13_example_20.html """

{% extends "base.html" %}
{% comment %}
By not using {% block stylesheets %}, this template inherits the
stylesheets block from the base.html parent, in this case the
default project.css link.
{% endcomment %}


"""chapter_13_example_21.html """

{# templates/toppings/topping_list.html #}
{# Using implicit names, good for code reuse #}
<ol>
{% for object in object_list %}
<li>{{ object }} </li>
{% endfor %}
</ol>

{# Using explicit names, good for object specific code #}
<ol>
{% for topping in topping_list %}
<li>{{ topping }} </li>
{% endfor %}
</ol>


"""chapter_13_example_22.html """

<a href="/flavors/">


"""chapter_13_example_23.html """

<a href="{% url 'flavors:list' %}">


"""chapter_13_example_24.py """

# settings/local.py
TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'APP_DIRS': True,
'OPTIONS':
'string_if_invalid': 'INVALID EXPRESSION: %s'
},
]


# Chapter 14: Template Tags and Filters

"""chapter_14_example_01.html """

{% extends "base.html" %}

{% load flavors_tags %}


"""chapter_14_example_02.py """

# settings/base.py
TEMPLATES = [
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'OPTIONS': {
# Don't do this!
# It's an evil anti-pattern!
'builtins': ['flavors.templatetags.flavors_tags'],
},
]


# Chapter 15: Django Templates and Jinja2

"""chapter_15_example_01.html """

<div style="display:none">
<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
</div>


"""chapter_15_example_02.py """

# core/jinja2.py
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import defaultfilters
from django.urls import reverse

from jinja2 import Environment

def environment(**options):
env = Environment(**options)
env.globals.update({
'static': staticfiles_storage.url,
'url': reverse,
'dj': defaultfilters
})
return env


"""chapter_15_example_03.html """

<table><tbody>
{% for purchase in purchase_list %}
<tr>
<a href="{{ url('purchase:detail', pk=purchase.pk) }}">
{{ purchase.title }}
</a>
</tr>
<tr>{{ dj.date(purchase.created, 'SHORT_DATE_FORMAT') }}</tr>
<tr>{{ dj.floatformat(purchase.amount, 2) }}</tr>
{% endfor %}
</tbody></table>


"""chapter_15_example_04.py """

# core/mixins.py
from django.template import defaultfilters

class DjFilterMixin:
dj = defaultfilters


"""chapter_15_example_05.html """

<table><tbody>
{% for purchase in purchase_list %}
<tr>
<a href="{{ url('purchase:detail', pk=purchase.pk) }}">
{{ purchase.title }}
</a>
</tr>
<!-- Call the django.template.defaultfilters functions from the view -->
<tr>{{ view.dj.date(purchase.created, 'SHORT_DATE_FORMAT') }}</tr>
<tr>{{ view.dj.floatformat(purchase.amount, 2) }}</tr>
{% endfor %}
</tbody></table>


"""chapter_15_example_06.py """

# core/jinja2.py
from jinja2 import Environment

import random

def environment(**options):
env = Environment(**options)
env.globals.update({
# Runs only on the first template load! The three displays below
#   will all present the same number.
#   {{ random_once }} {{ random_once }} {{ random_once }}
'random_once': random.randint(1, 5)
# Can be called repeated as a function in templates. Each call
#   returns a random number:
#   {{ random() }} {{ random() }} {{ random() }}
'random': lambda: random.randint(1, 5),
})
return env


# Chapter 16: Building REST APIs with Django REST Framework (NEW)

"""chapter_16_example_01.py """

REST_FRAMEWORK = {
'DEFAULT_PERMISSION_CLASSES': (
'rest_framework.permissions.IsAdminUser',
),
}


"""chapter_16_example_02.py """

# flavors/models.py
import uuid as uuid_lib

from django.db import models
from django.urls import reverse

class Flavor(models.Model):
title = models.CharField(max_length=255)
slug = models.SlugField(unique=True)  # Used to find the web URL
uuid = models.UUIDField( # Used by the API to look up the record
db_index=True,
default=uuid_lib.uuid4,
editable=False)
scoops_remaining = models.IntegerField(default=0)

def get_absolute_url(self):
return reverse('flavors:detail', kwargs={'slug': self.slug})


"""chapter_16_example_03.py """

# flavors/api/serializers.py
from rest_framework import serializers

from ..models import Flavor

class FlavorSerializer(serializers.ModelSerializer):
class Meta:
model = Flavor
fields = ['title', 'slug', 'uuid', 'scoops_remaining']


"""chapter_16_example_04.py """

# flavors/api/views.py
from rest_framework.generics import (
ListCreateAPIView,
RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from ..models import Flavor
from .serializers import FlavorSerializer

class FlavorListCreateAPIView(ListCreateAPIView):
queryset = Flavor.objects.all()
permission_classes = (IsAuthenticated, )
serializer_class = FlavorSerializer
lookup_field = 'uuid'  # Don't use Flavor.id!

class FlavorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
queryset = Flavor.objects.all()
permission_classes = (IsAuthenticated, )
serializer_class = FlavorSerializer
lookup_field = 'uuid'  # Don't use Flavor.id!


"""chapter_16_example_05.py """

# flavors/urls.py
from django.conf.urls import url

from flavors.api import views

urlpatterns = [
# /flavors/api/
url(
regex=r'^api/$',
view=views.FlavorListCreateAPIView.as_view(),
name='flavor_rest_api'
),
# /flavors/api/:slug/
url(
regex=r'^api/(?P<uuid>[-\w]+)/$',
view=views.FlavorRetrieveUpdateDestroyAPIView.as_view(),
name='flavor_rest_api'
)
]


"""chapter_16_example_06.txt """

flavors/api/
flavors/api/:uuid/


"""chapter_16_example_07.txt """

flavors/
├── api/
│   ├── __init__.py
│   ├── authentication.py
│   ├── parsers.py
│   ├── permissions.py
│   ├── renderers.py
│   ├── serializers.py
│   ├── validators.py
│   ├── views.py
│   ├── viewsets.py


"""chapter_16_example_08.txt """

flavors/
├── api/
│   ├── __init__.py
│   ├── ... other modules here
│   ├── views
│   │   ├── __init__.py
│   │   ├── flavor.py
│   │   ├── ingredient.py


"""chapter_16_example_09.txt """

api/flavors/ # GET, POST
api/flavors/:uuid/ # GET, PUT, DELETE
api/users/ # GET, POST
api/users/:uuid/ # GET, PUT, DELETE


"""chapter_16_example_10.py """

# core/api_urls.py
"""Called from the project root's urls.py URLConf thus:
url(r'^api/', include('core.api_urls', namespace='api')),
"""
from django.conf.urls import url

from flavors.api import views as flavor_views
from users.api import views as user_views

urlpatterns = [
# {% url 'api:flavors' %}
url(
regex=r'^flavors/$',
view=flavor_views.FlavorCreateReadView.as_view(),
name='flavors'
),
# {% url 'api:flavors' flavor.uuid %}
url(
regex=r'^flavors/(?P<uuid>[-\w]+)/$',
view=flavor_views.FlavorReadUpdateDeleteView.as_view(),
name='flavors'
),
# {% url 'api:users' %}
url(
regex=r'^users/$',
view=user_views.UserCreateReadView.as_view(),
name='users'
),
# {% url 'api:users' user.uuid %}
url(
regex=r'^users/(?P<uuid>[-\w]+)/$',
view=user_views.UserReadUpdateDeleteView.as_view(),
name='users'
),
]



"""chapter_16_example_11.py """

# sundaes/api/views.py
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Sundae, Syrup
from .serializers import SundaeSerializer, SyrupSerializer

class PourSyrupOnSundaeView(APIView):
"""View dedicated to adding syrup to sundaes"""

def post(self, request, *args, **kwargs):
# Process pouring of syrup here,
# Limit each type of syrup to just one pour
# Max pours is 3 per sundae
sundae = get_object_or_404(Sundae, uuid=request.data['uuid'])
try:
sundae.add_syrup(request.data['syrup'])
except Sundae.TooManySyrups:
msg = "Sundae already maxed out for syrups"
return Response({'message': msg}, status_code=400)
except Syrup.DoesNotExist
msg = "{}  does not exist".format(request.data['syrup'])
return Response({'message': msg}, status_code=404)
return Response(SundaeSerializer(sundae).data)

def get(self, request, *args, **kwargs)
# Get list of syrups already poured onto the sundae
sundae = get_object_or_404(Sundae, uuid=request.data['uuid'])
syrups = [SyrupSerializer(x).data for x in sundae.syrup_set.all()]
return Response(syrups)


"""chapter_16_example_12.txt """

/sundae/  # GET, POST
/sundae/:uuid/  # PUT, DELETE
/sundae/:uuid/syrup/  # GET, POST
/syrup/  # GET, POST
/syrup/:uuid/  # PUT, DELETE


"""chapter_16_example_13.txt """

/api/cones/  # GET, POST
/api/cones/:uuid/  # PUT, DELETE
/api/scoops/  # GET, POST
/api/scoops/:uuid/  # PUT, DELETE


"""chapter_16_example_14.txt """

/api/cones/  # GET, POST
/api/cones/:uuid/  # PUT, DELETE
/api/cones/:uuid/scoops/  # GET, POST
/api/cones/:uuid/scoops/:uuid/  # PUT, DELETE
/api/scoops/  # GET, POST
/api/scoops/:uuid/  # PUT, DELETE


"""chapter_16_example_15.py """

# core/apiv1_shutdown.py
from django.http import HttpResponseGone

apiv1_gone_msg = """APIv2 was removed on April 2, 2017. Please switch to APIv3:
<ul>
<li>
<a href="https://www.example.com/api/v3/">APIv3 Endpoint</a>
</li>
<li>
<a href="https://example.com/apiv3_docs/">APIv3 Documentation</a>
</li>
<li>
<a href="http://example.com/apiv1_shutdown/">APIv1 shut down notice</a>
</li>
</ul>
"""

def apiv1_gone(request):
return HttpResponseGone(apiv1_gone_msg)


# Chapter 17: Consuming REST APIs

"""chapter_17_example_01.html """

<html>
<!-- Placed anywhere in the page, doesn't even need to
be in a form as the input element is hidden -->
{% csrf_token %}
</html>


"""chapter_17_example_02.txt """

var csrfToken = $('[name=csrfmiddlewaretoken]').val();
var formData = {
csrfmiddlewaretoken: csrfToken,
name=name, age=age
};
$.ajax({
url: '/api/do-something/'',
data: formData,
type: 'POST'
})


# Chapter 19: Working With the Django Admin

"""chapter_19_example_01.py """

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # For Python 3.5+ and 2.7
class IceCreamBar(models.Model):
name = models.CharField(max_length=100)
shell = models.CharField(max_length=100)
filling = models.CharField(max_length=100)
has_stick = models.BooleanField(default=True)

def __str__(self):
return self.name


"""chapter_19_example_02.py """

>>> IceCreamBar.objects.all()
[<IceCreamBar: Vanilla Crisp>, <IceCreamBar: Mint Cookie Crunch>,
<IceCreamBar: Strawberry Pie>]


"""chapter_19_example_03.py """

from django.contrib import admin

from .models import IceCreamBar

@admin.register(IceCreamBar)
class IceCreamBarModelAdmin(admin.ModelAdmin):
list_display = ('name', 'shell', 'filling')


"""chapter_19_example_04.py """

# icecreambars/admin.py
from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html

from .models import IceCreamBar

@admin.register(IceCreamBar)
class IceCreamBarModelAdmin(admin.ModelAdmin):
list_display = ('name', 'shell', 'filling')
readonly_fields = ('show_url',)

def show_url(self, instance):
url = reverse('ice_cream_bar_detail', kwargs={'pk': instance.pk})
response = format_html("""<a href="{0}">{0}</a>""", url)
return response

show_url.short_description = 'Ice Cream Bar URL'
# Displays HTML tags
# Never set allow_tags to True against user submitted data!!!
show_url.allow_tags = True


# Chapter 20: Dealing with the User Model

"""chapter_20_example_01.py """

# Stock user model definition
>>> from django.contrib.auth import get_user_model
>>> get_user_model()
<class django.contrib.auth.models.User>

# When the project has a custom user model definition
>>> from django.contrib.auth import get_user_model
>>> get_user_model()
<class profiles.models.UserProfile>


"""chapter_20_example_02.py """

from django.conf import settings
from django.db import models

class IceCreamStore(models.Model):

owner = models.OneToOneField(settings.AUTH_USER_MODEL)
title = models.CharField(max_length=255)


"""chapter_20_example_03.py """

# DON'T DO THIS!
from django.contrib.auth import get_user_model
from django.db import models

class IceCreamStore(models.Model):

# This following line tends to create import loops.
owner = models.OneToOneField(get_user_model())
title = models.CharField(max_length=255)


"""chapter_20_example_04.py """

# profiles/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class KarmaUser(AbstractUser):
karma = models.PositiveIntegerField(verbose_name='karma',
default=0,
blank=True)


"""chapter_20_example_05.py """

AUTH_USER_MODEL = 'profiles.KarmaUser'


"""chapter_20_example_06.py """

# profiles/models.py

from django.conf import settings
from django.db import models

from flavors.models import Flavor

class EaterProfile(models.Model):

# Default user profile
# If you do this you need to either have a post_save signal or
#     redirect to a profile_edit view on initial login.
user = models.OneToOneField(settings.AUTH_USER_MODEL)
favorite_ice_cream = models.ForeignKey(Flavor, null=True, blank=True)

class ScooperProfile(models.Model):

user = models.OneToOneField(settings.AUTH_USER_MODEL)
scoops_scooped = models.IntegerField(default=0)

class InventorProfile(models.Model):

user = models.OneToOneField(settings.AUTH_USER_MODEL)
flavors_invented = models.ManyToManyField(Flavor, null=True, blank=True)




# Chapter 21: Django's Secret Sauce: Third-Party Packages

"""chapter_21_example_01.txt """

Django==1.11
coverage==4.3.4
django-extensions==1.7.6
django-braces==1.11


"""chapter_21_example_02.txt """


-e git+https://github.com/erly-adptr/py-junk.git#egg=py-jnk


"""chapter_21_example_03.txt """

# DON'T DO THIS!
# requirements for django-blarg

Django==1.10.2
requests==1.2.3


"""chapter_21_example_04.txt """

# requirements.txt for the mythical web site 'icecreamratings.com'
Django==1.11
requests==2.13.0
django−blarg==1.0

# Note that unlike the django−blarg library , we explicitly pin
# the requirements so we have total control over the environment


"""chapter_21_example_05.txt """

# requirements for django-blarg

Django>=1.10,<1.12
requests>=2.6.0,<=2.13.0


"""chapter_21_example_06.txt """

# Only if you haven't installed cookiecutter yet
$ pip install cookiecutter

# Creating a Django Package from scratch
$ cookiecutter https://github.com/pydanny/cookiecutter-djangopackage.git

# Creating a Python Package from scratch
$ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git


"""chapter_21_example_07.txt """

$ pip install twine
$ python setup.py sdist
$ twine upload dist/*



"""chapter_21_example_08.txt """

$ pip install wheel


"""chapter_21_example_09.txt """

$ python setup.py bdist_wheel
$ twine upload dist/*


"""chapter_21_example_10.txt """

# setup.cfg
[wheel]
universal = 1


# Chapter 22: Testing Chapter of Doom!

"""chapter_22_example_01.txt """

popsicles/
__init__.py
admin.py
forms.py
models.py
tests/
__init__.py
test_forms.py
test_models.py
test_views.py
views.py


"""chapter_22_example_02.py """

# flavors/tests/test_api.py
import json

from django.test import TestCase
from django.urls import reverse

from flavors.models import Flavor

class FlavorAPITests(TestCase):

def setUp(self):
Flavor.objects.get_or_create(title='A Title', slug='a-slug')

def test_list(self):
url = reverse('flavor_object_api')
response = self.client.get(url)
self.assertEquals(response.status_code, 200)
data = json.loads(response.content)
self.assertEquals(len(data), 1)


"""chapter_22_example_03.py """

# flavors/tests/test_api.py
import json

from django.test import TestCase
from django.urls import reverse

from flavors.models import Flavor

class DjangoRestFrameworkTests(TestCase):

def setUp(self):
Flavor.objects.get_or_create(title='title1', slug='slug1')
Flavor.objects.get_or_create(title='title2', slug='slug2')

self.create_read_url = reverse('flavor_rest_api')
self.read_update_delete_url = \
reverse('flavor_rest_api', kwargs={'slug': 'slug1'})

def test_list(self):
response = self.client.get(self.create_read_url)

# Are both titles in the content?
self.assertContains(response, 'title1')
self.assertContains(response, 'title2')

def test_detail(self):
response = self.client.get(self.read_update_delete_url)
data = json.loads(response.content)
content = {'id': 1, 'title': 'title1', 'slug': 'slug1',
'scoops_remaining': 0}
self.assertEquals(data, content)

def test_create(self):
post = {'title': 'title3', 'slug': 'slug3'}
response = self.client.post(self.create_read_url, post)
data = json.loads(response.content)
self.assertEquals(response.status_code, 201)
content = {'id': 3, 'title': 'title3', 'slug': 'slug3',
'scoops_remaining': 0}
self.assertEquals(data, content)
self.assertEquals(Flavor.objects.count(), 3)

def test_delete(self):
response = self.client.delete(self.read_update_delete_url)
self.assertEquals(response.status_code, 204)
self.assertEquals(Flavor.objects.count(), 1)


"""chapter_22_example_04.py """

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory

from .views import cheese_flavors

def add_middleware_to_request(request, middleware_class):
middleware = middleware_class()
middleware.process_request(request)
return request

def add_middleware_to_response(request, middleware_class):
middleware = middleware_class()
middleware.process_response(request)
return request

class SavoryIceCreamTest(TestCase):
def setUp(self):
# Every test needs access to the request factory.
self.factory = RequestFactory()

def test_cheese_flavors(self):
request = self.factory.get('/cheesy/broccoli/')
request.user = AnonymousUser()

# Annotate the request object with a session
request = add_middleware_to_request(request, SessionMiddleware)
request.session.save()

# process and test the request
response = cheese_flavors(request)
self.assertContains(response, 'bleah!')


"""chapter_22_example_05.py """

from unittest import mock, TestCase

import icecreamapi

from flavors.exceptions import CantListFlavors
from flavors.utils import list_flavors_sorted

class TestIceCreamSorting(TestCase):

# Set up monkeypatch of icecreamapi.get_flavors()
@mock.patch.object(icecreamapi, 'get_flavors')
def test_flavor_sort(self, get_flavors):
# Instructs icecreamapi.get_flavors() to return an unordered list.
get_flavors.return_value = ['chocolate', 'vanilla', 'strawberry', ]

# list_flavors_sorted() calls the icecreamapi.get_flavors()
#   function. Since we've monkeypatched the function,  it will always
#   return ['chocolate', 'strawberry', 'vanilla', ]. Which the.
#   list_flavors_sorted() will sort alphabetically
flavors = list_flavors_sorted()

self.assertEqual(
flavors,
['chocolate', 'strawberry', 'vanilla', ]

)


"""chapter_22_example_06.py """

@mock.patch.object(icecreamapi, 'get_flavors')
def test_flavor_sort_failure(self, get_flavors):
# Instructs icecreamapi.get_flavors() to throw a FlavorError.
get_flavors.side_effect = icecreamapi.FlavorError()

# list_flavors_sorted() catches the icecreamapi.FlavorError()
#   and passes on a CantListFlavors exception.
with self.assertRaises(CantListFlavors):
list_flavors_sorted()


"""chapter_22_example_07.py """

@mock.patch.object(requests, 'get')
def test_request_failure(self, get)
"""Test if the target site is innaccessible."""
get.side_effect = requests.exception.ConnectionError()

with self.assertRaises(CantListFlavors):
list_flavors_sorted()

@mock.patch.object(requests, 'get')
def test_request_failure(self, get)
"""Test if we can handle SSL problems elegantly."""
get.side_effect = requests.exception.SSLError()

with self.assertRaises(CantListFlavors):
list_flavors_sorted()


"""chapter_22_example_08.txt """

$ coverage run manage.py test --settings=twoscoops.settings.test


"""chapter_22_example_09.txt """

Creating test database for alias "default"...
..
-----------------------------------------------
Ran 2 tests in 0.008s

OK

Destroying test database for alias "default"...


"""chapter_22_example_10.txt """

$ coverage html --omit="admin.py"


"""chapter_22_example_11.py """

# test_models.py
from pytest import raises

from cones.models import Cone

def test_good_choice():
assert Cone.objects.filter(type='sugar').count() == 1

def test_bad_cone_choice():
with raises(Cone.DoesNotExist):
Cone.objects.get(type='spaghetti')


# Chapter 23: Documentation: Be Obsessed

"""chapter_23_example_01.txt """

Section Header
==============

**emphasis (bold/strong)**

*italics*

Simple link: https://twoscoopspress.com
Fancier Link: `Two Scoops of Django`_

.. _Two Scoops of Django: https://twoscoopspress.com

Subsection Header
-----------------

#) An enumerated list item

#) Second item

* First bullet

* Second bullet

* Indented Bullet

* Note carriage return and indents

Literal code block::

def like():
print("I like Ice Cream")

for i in range(10):
like()

Python colored code block (requires pygments):

code-block:: python

# You need to "pip install pygments" to make this work.

for i in range(10):
like()

JavaScript colored code block:

code-block:: javascript

console.log("Don't use alert()");



"""chapter_23_example_02.py """

# setup.py
import subprocess
import sys

if sys.argv[-1] == 'md2rst':
subprocess.call('pandoc README.md -o README.rst', shell=True)
...


# Chapter 26: Logging: What's It For, Anyway?

"""chapter_26_example_01.py """

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


"""chapter_26_example_02.txt """

Strict-Transport-Security: max-age=31536000; includeSubDomains


"""chapter_26_example_03.py """

from django import forms

class SpecialForm(forms.Form):
my_secret = forms.CharField(
widget=forms.TextInput(attrs={'autocomplete': 'off'}))


"""chapter_26_example_04.py """

from django import forms

class SecretInPublicForm(forms.Form):

my_secret = forms.CharField(widget=forms.PasswordInput())


"""chapter_26_example_05.py """

# stores/models.py
from django.conf import settings
from django.db import models

class Store(models.Model):
title = models.CharField(max_length=255)
slug = models.SlugField()
owner = models.ForeignKey(settings.AUTH_USER_MODEL)
# Assume 10 more fields that cover address and contact info.


"""chapter_26_example_06.py """

# DON'T DO THIS!
from django import forms

from .models import Store

class StoreForm(forms.ModelForm):

class Meta:
model = Store
# DON'T DO THIS: Implicit definition of fields.
#                Too easy to make mistakes!
excludes = ("pk", "slug", "modified", "created", "owner")


"""chapter_26_example_07.py """

from django import forms

from .models import Store

class StoreForm(forms.ModelForm):

class Meta:
model = Store
# Explicitly specifying the fields we want
fields = (
"title", "address_1", "address_2", "email",
"usstate", "postal_code", "city",
)


"""chapter_26_example_08.py """

# stores/models.py
from django.conf import settings
from django.db import models

class Store(models.Model):
title = models.CharField(max_length=255)
slug = models.SlugField()
owner = models.ForeignKey(settings.AUTH_USER_MODEL)
co_owners = models.ManyToManyField(settings.AUTH_USER_MODEL)
# Assume 10 more fields that cover address and contact info.


"""chapter_26_example_09.py """

import uuid as uuid_lib
from django.db import models

class IceCreamPayment(models.Model):
uuid = models.UUIDField(
db_index=True,
default=uuid_lib.uuid4,
editable=False)

def __str__(self):
return str(self.pk)


"""chapter_26_example_10.py """

>>> from payments import IceCreamPayment
>>> payment = IceCreamPayment()
>>> IceCreamPayment.objects.get(id=payment.id)
<IceCreamPayment: 1>
>>> payment.uuid
UUID('0b0fb68e-5b06-44af-845a-01b6df5e0967')
>>> IceCreamPayment.objects.get(uuid=payment.uuid)
<IceCreamPayment: 1>


# Chapter 27: Signals: Use Cases and Avoidance Techniques

"""chapter_27_example_01.py """

# Taken directly from core Django code.
# Used here to illustrate an example only, so don't
# copy this into your project.
logger.error('Internal Server Error: %s', request.path,
exc_info=exc_info,
extra={
'status_code': 500,
'request': request
}
)


"""chapter_27_example_02.py """

# Taken directly from core Django code.
# Used here to illustrate an example only, so don't
# copy this into your project.
logger.warning('Forbidden (%s): %s',
REASON_NO_CSRF_COOKIE, request.path,
extra={
'status_code': 403,
'request': request,
}
)


"""chapter_27_example_03.py """

from django.views.generic import TemplateView

from .helpers import pint_counter

class PintView(TemplateView):

def get_context_data(self, *args, **kwargs):
context = super(PintView, self).get_context_data(**kwargs)
pints_remaining = pint_counter()
print('Only %d pints of ice cream left.' % (pints_remaining))
return context



"""chapter_27_example_04.py """

import logging

from django.views.generic import TemplateView

from .helpers import pint_counter

logger = logging.getLogger(__name__)

class PintView(TemplateView):

def get_context_data(self, *args, **kwargs):
context = super(PintView, self).get_context_data(**kwargs)
pints_remaining = pint_counter()
logger.debug('Only %d pints of ice cream left.' % pints_remaining)
return context


"""chapter_27_example_05.py """

import logging
import requests

logger = logging.getLogger(__name__)

def get_additional_data():
try:
r = requests.get('http://example.com/something-optional/')
except requests.HTTPError as e:
logger.exception(e)
logger.debug('Could not get additional data', exc_info=True)
return None
return r


"""chapter_27_example_06.py """

# You can place this snippet at the top
# of models.py, views.py, or any other
# file where you need to log.
import logging

logger = logging.getLogger(__name__)


# Chapter 28: What About Those Random Utilities?

"""chapter_28_example_01.py """

# events/managers.py
from django.db import models

class EventManager(models.Manager):

def create_event(self, title, start, end, creator):
event = self.model(title=title,
start=start,
end=end,
creator=creator)
event.save()
event.notify_admins()
return event



"""chapter_28_example_02.py """

# events/models.py
from django.conf import settings
from django.core.mail import mail_admins
from django.db import models

from model_utils.models import TimeStampedModel

from .managers import EventManager

class Event(TimeStampedModel):

STATUS_UNREVIEWED, STATUS_REVIEWED = (0, 1)
STATUS_CHOICES = (
(STATUS_UNREVIEWED, "Unreviewed"),
(STATUS_REVIEWED, "Reviewed"),
)

title = models.CharField(max_length=100)
start = models.DateTimeField()
end = models.DateTimeField()
status = models.IntegerField(choices=STATUS_CHOICES,
default=STATUS_UNREVIEWED)
creator = models.ForeignKey(settings.AUTH_USER_MODEL)

objects = EventManager()

def notify_admins(self):
# create the subject and message
subject = "{user} submitted a new event!".format(
user=self.creator.get_full_name())
message = """TITLE: {title}
START: {start}
END: {end}""".format(title=self.title, start=self.start,
end=self.end)

# Send to the admins!
mail_admins(subject=subject,
message=message,
fail_silently=False)


"""chapter_28_example_03.txt """

>>> from django.contrib.auth import get_user_model
>>> from django.utils import timezone
>>> from events.models import Event
>>> user = get_user_model().objects.get(username="audreyr")
>>> now = timezone.now()
>>> event = Event.objects.create_event(
...     title="International Ice Cream Tasting Competition",
...     start=now,
...     end=now,
...     user=user
...     )


# Chapter 29: Deployment: Platforms as a Service

"""chapter_29_example_01.txt """

core/
__init__.py
managers.py  # contains the custom model manager(s)
models.py
views.py  # Contains the custom view mixin(s)


"""chapter_29_example_02.py """

from core.managers import PublishedManager
from core.views import IceCreamMixin


"""chapter_29_example_03.py """

>>> from django.utils.text import slugify
>>> slugify('straße') # German
'strae'


"""chapter_29_example_04.py """

>>> slugify('straße', allow_unicode=True) # Again with German
'straße'


"""chapter_29_example_05.py """

# core/utils.py
from django.core.exceptions import ObjectDoesNotExist

class BorkedObject:
loaded = False

def generic_load_tool(model, pk):
try:
instance = model.objects.get(pk=pk)
except ObjectDoesNotExist:
return BorkedObject()
instance.loaded = True
return instance


"""chapter_29_example_06.py """

# core/utils.py
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied

def get_object_or_403(model, **kwargs):
try:
return model.objects.get(**kwargs)
except ObjectDoesNotExist:
raise PermissionDenied
except MultipleObjectsReturned:
raise PermissionDenied


"""chapter_29_example_07.py """

# stores/calc.py

def finance_data_adjudication(store, sales, issues):

if store.something_not_right:
msg = 'Something is not right. Please contact the support team.'
raise PermissionDenied(msg)

# Continue on to perform other logic.


"""chapter_29_example_08.py """

# urls.py

# This demonstrates the use of a custom permission denied view. The default
# view is django.views.defaults.permission_denied
handler403 = 'core.views.permission_denied_view'


"""chapter_29_example_09.py """

# serializer_example.py
from django.core.serializers import get_serializer

from favorites.models import Favorite

# Get and instantiate the serializer class
# The 'json' can be replaced with 'python' or 'xml'.
# If you have pyyaml installed, you can replace it with
#   'pyyaml'
JSONSerializer = get_serializer('json')
serializer = JSONSerializer()

favs = Favorite.objects.filter()[:5]

# Serialize model data
serialized_data = serializer.serialize(favs)

# save the serialized data for use in the next example
with open('data.json', 'w') as f:
f.write(serialized_data)



"""chapter_29_example_10.py """

# deserializer_example.py
from django.core.serializers import get_serializer

from favorites.models import Favorite

# Get and instantiate the serializer class
# The 'json' can be replaced with 'python' or 'xml'.
# If you have pyyaml installed, you can replace it with
#   'pyyaml'
JSONSerializer = get_serializer('json')
serializer = JSONSerializer()

# open the serialized data file
with open('data.txt') as f:
serialized_data = f.read()

# deserialize model data into a generator object
#   we'll call 'python data'
python_data = serializer.deserialize(serialized_data)

# iterate through the python_data
for element in python_data:
# Prints 'django.core.serializers.base.DeserializedObject'
print(type(element))

# Elements have an 'object' that are literally instantiated
#   model instances (in this case, favorites.models.Favorite)
print(
element.object.pk,
element.object.created
)



"""chapter_29_example_11.py """

# json_encoding_example.py
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

data = {'date': timezone.now()}

# If you don't add the DjangoJSONEncoder class then
# the json library will throw a TypeError.
json_data = json.dumps(data, cls=DjangoJSONEncoder)

print(json_data)


# Chapter 33: Where and How to Ask Django Questions

"""chapter_33_example_01.txt """

twoscoopspress$ python discounts/manage.py runserver 8001
Starting development server at http://127.0.0.1:8001/
Quit the server with CONTROL-C.

Internal Server Error: /
Traceback (most recent call last):
File "/.envs/oc/lib/python.7/site-packages/django/core/handlers/base.py",
line 132, in get_response response = wrapped_callback(request,
*callback_args, **callback_kwargs)
File "/.envs/oc/lib/python.7/site-packages/django/utils/decorators.py",
line 145, in inner
return func(*args, **kwargs)
TypeError: __init__() takes exactly 1 argument (2 given)


"""chapter_33_example_02.py """

# Forgetting the 'as_view()' method
url(r'^$',  HomePageView, name='home'),


"""chapter_33_example_03.py """

url(r'^$',  HomePageView.as_view(), name='home'),


"""chapter_33_example_04.html """

<form action="{% url 'stores:file_upload' store.pk %}"
method="post"
enctype="multipart/form-data">


"""chapter_33_example_05.py """

# stores/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from stores.forms import UploadFileForm
from stores.models import Store

def upload_file(request, pk):
"""Simple FBV example"""
store = get_object_or_404(Store, pk=pk)
if request.method == 'POST':
# Don't forget to add request.FILES!
form = UploadFileForm(request.POST, request.FILES)
if form.is_valid():
store.handle_uploaded_file(request.FILES['file'])
return redirect(store)
else:
form = UploadFileForm()
return render(request, 'upload.html', {'form': form, 'store': store})


"""chapter_33_example_06.py """

# stores/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from stores.forms import UploadFileForm
from stores.models import Store

class UploadFile(View):
"""Simple CBV example"""
def get_object(self):
return get_object_or_404(Store, pk=self.kwargs['pk'])

def post(self, request, *args, **kwargs):
store = self.get_object()
form = UploadFileForm(request.POST, request.FILES)
if form.is_valid():
store.handle_uploaded_file(request.FILES['file'])
return redirect(store)
return redirect('stores:file_upload', pk=pk)

def get(self, request, *args, **kwargs):
store = self.get_object()
form = UploadFileForm()
return render(
request,
'upload.html',
{'form': form, 'store': store})


"""chapter_33_example_07.py """

# core/middleware.py
import sys

from django.views.debug import technical_500_response

class UserBasedExceptionMiddleware:
def process_exception(self, request, exception):
if request.user.is_superuser:
return technical_500_response(request, *sys.exc_info())


"""chapter_33_example_08.py """

# settings.py
ALLOWED_HOSTS = [
'.djangopackages.org',
'.djangopackages.com',
]


