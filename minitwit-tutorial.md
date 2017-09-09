- User based models

```python
class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')

    class Meta:
        unique_together = ('follower', 'followed')


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000)
    pub_date = models.DateTimeField(auto_now_add=True)
```

- Use the `timeline` template multiple times and make 3 views

```
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.views import View

from .models import Message
from .forms import UserForm, LoginForm


def get_paged_posts(request, posts, n=5):
    paginator = Paginator(posts, n)
    page = request.GET.get('page')
    try:
        paged_posts = paginator.page(page)
    except PageNotAnInteger:
        paged_posts = paginator.page(1)
    except EmptyPage:
        paged_posts = paginator.page(paginator.num_pages)
    return paged_posts


class MyTimeline(LoginRequiredMixin, View):
    login_url = '/public'
    redirect_field_name = ''

    def get(self, request):
        followed_users = request.user.follower_set.values_list('followed', flat=True)
        all_users = list(followed_users) + [request.user]
        posts = Message.objects.filter(author__in=all_users).order_by('-pub_date')
        paged_posts = get_paged_posts(request, posts)
        return render(request, 'timeline.html', {'posts': paged_posts})

    def post(self, request):
        if request.POST.get('text'):
            request.user.message_set.create(text=request.POST.get('text'))
        return self.get(request)


def public_timeline(request):
    posts = Message.objects.order_by('-pub_date')
    paged_posts = get_paged_posts(request, posts)
    return render(request, 'timeline.html', {'posts': paged_posts})


def user_timeline(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile_user_posts = profile_user.message_set.order_by('-pub_date')
    is_followed = False
    if hasattr(request.user, 'follower_set') and request.user.follower_set.filter(followed=profile_user).exists():
        is_followed = True
    paged_posts = get_paged_posts(request, profile_user_posts)
    return render(request, 'timeline.html',
                  {'posts': paged_posts, 'profile_user': profile_user, 'followed': is_followed})


@login_required
def follow_user(request, username):
    followed = get_object_or_404(User, username=username)
    request.user.follower_set.create(followed=followed)
    return redirect('user_timeline', username=username)


@login_required
def unfollow_user(request, username):
    followed = get_object_or_404(User, username=username)
    request.user.follower_set.filter(followed=followed).delete()
    return redirect('user_timeline', username=username)


def login_view(request):
    if request.user.is_authenticated():
        return redirect('timeline')
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect('timeline')
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.user.is_authenticated():
        return redirect('timeline')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You were successfully registered and can login now')
            return redirect('login_view')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You were logger out')
    return redirect('public_timeline')
```


- Repeat to use the `timeline` template multiple times 
```html
{% extends "layout.html" %}
{% load app_filters %}
{% block body %}

    {% with request.resolver_match.url_name as url_name %}
        {% if url_name == 'public_timeline' %}
            <h2> Public Timeline </h2>
        {% elif url_name == 'user_timeline' %}
            <h2> {{ profile_user.username }}'s Timeline </h2>
            {% if user.is_authenticated %}
                <div class="followstatus">
                    {% if user == profile_user %}
                        This is you!
                    {% elif followed %}
                        You are currently following this user.
                        <a class="unfollow" href="{% url 'unfollow_user' profile_user.username %}">Unfollow user</a>
                        .
                    {% else %}
                        You are not yet following this user.
                        <a class="follow" href="{% url 'follow_user' profile_user.username %}">Follow user</a>.
                    {% endif %}
                </div>
            {% endif %}
        {% else %}
            <h2>My Timeline </h2>
            <div class="row">
                <div class="col-lg-6 col-lg-offset-3">
                    <div class="form-group">
                        <label>What's on your mind ?</label>
                        <form action="{% url 'timeline' %}" method="post">
                            {% csrf_token %}
                            <p>
                                <input type="text" name="text" size="60">
                                <button type="submit" class="btn btn-default">Share</button>
                        </form>
                    </div>
                </div>
            </div>
        {% endif %}
    {% endwith %}

    {% if posts %}
        {% for post in posts %}
            <div class="row">
                <div class="col-lg-6 col-lg-offset-3">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <img src="{{ post.author.email|gravatar }}">
                            <strong><a
                                    href="{% url 'user_timeline' post.author.username %}">{{ post.author.username }}</a></strong>
                        </div>
                        <div class="panel-body">
                            {{ post.text | safe }}
                            <small>&mdash; {{ post.pub_date|datetimeformat }}</small>
                        </div>
                    </div>
                </div>
            </div>
        {% endfor %}
    {% else %}
        <div class="row">
            <div class="col-lg-6 col-lg-offset-3">
                There is no valid post yet.
            </div>
        </div>
    {% endif %}


    <div class="row">
        <div class="col-lg-6 col-lg-offset-3">
            <ul class="pagination pagination-centered">
                {% if posts.has_previous %}
                    <li><a href="?page=1"><<</a></li>
                    `
                    <li><a href="?page={{ posts.previous_page_number }}"><</a></li>
                {% endif %}

                {% for i in posts.paginator.page_range %}
                    <li {% if posts.number == i %} class="active" {% endif %}><a href="?page={{ i }}">{{ i }}</a></li>
                {% endfor %}

                {% if posts.has_next %}
                    <li><a href="?page={{ posts.next_page_number }}">></a></li>
                    <li><a href="?page={{ posts.paginator.num_pages }}">>></a></li>
                {% endif %}
            </ul>
        </div>
    </div>


{% endblock %}

```

- Setting
```python
import os
from sys import platform
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&uqx3rb^g6-_fw#%iz6u@p1*oz0ng6r8gj$una=lb4h(__g3+v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',
    'ckeditor',
    'ckeditor_uploader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'minitwit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'minitwit.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)

# Authorize the use of the static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

GOOGLE_RECAPTCHA_SECRET_KEY = '6LfBcSkUAAAAAE7AbseHmOUBwEDoIcwkljzPjm0F'

LOGIN_URL = '/public'
LOGIN_REDIRECT_URL = ''

# Only for ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(tempfile.gettempdir(), 'ck_media')
CKEDITOR_IMAGE_BACKEND = "pillow"

# New
IMAGE_QUALITY = 40
THUMBNAIL_SIZE = (300, 300)

if platform == "darwin":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': "minitwit",
            'HOST': "localhost"
        }
    }
```

- Template and tag
```
from django import template
from hashlib import md5
from django.utils import timezone

register = template.Library()


@register.filter(name='gravatar')
def gravatar_url(email):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % (md5(email.strip().lower().encode('utf-8')).hexdigest(), 45)


@register.filter(name='datetimeformat')
def format_datetime(datetime):
    """Format a timestamp for display."""
    return timezone.localtime(datetime).strftime('%Y-%m-%d @ %H:%M')
```

- Admin
```python
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'text', 'pub_date', 'tags']
```

- URLs
```
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^$', views.MyTimeline.as_view(), name='my_timeline'),
    url(r'public/', views.public_timeline, name='public_timeline'),
    url(r'^user/(?P<username>\w+)/toggle/', views.toggle_following, name='toggle'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^login/$', views.Login.as_view(), name='login_view'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^user/(?P<username>\w+)/', views.user_timeline, name='user_timeline'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
```

- Forms
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self):
        user = User.objects.create_user(self.cleaned_data["username"], self.cleaned_data["email"],
                                        self.cleaned_data["password1"])
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def login(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return user
        
 ```
