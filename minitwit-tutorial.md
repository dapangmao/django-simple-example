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

    <h2>
        {% if request.resolver_match.url_name == 'public_timeline' %}
            Public Timeline
        {% elif request.resolver_match.url_name == 'user_timeline' %}
            {{ profile_user.username }}'s Timeline
        {% else %}
            My Timeline
        {% endif %}

    </h2>
    {% if user.is_authenticated %}
        {% if request.resolver_match.url_name == 'user_timeline' %}
            <div class="followstatus">
                {% if user == profile_user %} This is you!
                {% elif followed %} You are currently following this user.
                    <a class="unfollow" href="{% url 'unfollow_user' profile_user.username %}">Unfollow user</a>
                    .
                {% else %} You are not yet following this user.
                    <a class="follow" href="{% url 'follow_user' profile_user.username %}">Follow user</a>.
                {% endif %}
            </div>

        {% elif request.resolver_match.url_name == 'timeline' %}
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
    {% endif %}


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

- Use the `timeline` template multiple times 
    - the template can detect url by `request.resolver_match.url_name `
    
    
```html
{% extends "layout.html" %}
{% load app_filters %}
{% block body %}

    <h2>
        {% if request.resolver_match.url_name == 'public_timeline' %}
            Public Timeline
        {% elif request.resolver_match.url_name == 'user_timeline' %}
            {{ profile_user.username }}'s Timeline
        {% else %}
            My Timeline
        {% endif %}

    </h2>
    {% if user.is_authenticated %}
        {% if request.resolver_match.url_name == 'user_timeline' %}
            <div class="followstatus">
                {% if user == profile_user %} This is you!
                {% elif followed %} You are currently following this user.
                    <a class="unfollow" href="{% url 'unfollow_user' profile_user.username %}">Unfollow user</a>
                    .
                {% else %} You are not yet following this user.
                    <a class="follow" href="{% url 'follow_user' profile_user.username %}">Follow user</a>.
                {% endif %}
            </div>

        {% elif request.resolver_match.url_name == 'timeline' %}
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
    {% endif %}


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

- URLs

```python
urlpatterns = [
    url(r'^$', views.MyTimeline.as_view(), name='timeline'),
    url(r'public/', views.public_timeline, name='public_timeline'),
    url(r'^user/(?P<username>\w+)/unfollow/', views.unfollow_user, name='unfollow_user'),
    url(r'^user/(?P<username>\w+)/follow/', views.follow_user, name='follow_user'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user/(?P<username>\w+)/', views.user_timeline, name='user_timeline'),
    url(r'^admin/', include(admin.site.urls)),
]
```
