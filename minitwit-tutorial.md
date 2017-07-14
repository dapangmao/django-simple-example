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
