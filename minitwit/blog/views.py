import requests
from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.views import View

from .models import Message, Follower
from .forms import UserForm, LoginForm


def get_paged_posts(request, posts, n=5):
    paginator = Paginator(posts, n)
    page = request.GET.get('page')  # it will parse the page argument
    try:
        paged_posts = paginator.page(page)
    except PageNotAnInteger:
        paged_posts = paginator.page(1)
    except EmptyPage:
        paged_posts = paginator.page(paginator.num_pages)
    # The limitation could be given by
    # https://stackoverflow.com/questions/30864011/display-only-some-of-the-page-numbers-by-django-pagination
    return paged_posts


class MyTimeline(LoginRequiredMixin, View):
    def get(self, request):
        followed_users = request.user.follower_set.values_list('followed', flat=True)
        all_users = list(followed_users) + [request.user]
        posts = Message.objects.filter(author__in=all_users).order_by('-pub_date').select_related('author')
        paged_posts = get_paged_posts(request, posts)
        return render(request, 'blog/timeline.html', {'posts': paged_posts})

    def post(self, request):
        text = request.POST.get('text')
        if text:
            request.user.message_set.create(text=text)
        return self.get(request)


def public_timeline(request):
    posts = Message.objects.all().order_by('-pub_date').select_related('author')
    paged_posts = get_paged_posts(request, posts)
    return render(request, 'blog/timeline.html', {'posts': paged_posts})


def user_timeline(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile_user_posts = profile_user.message_set.order_by('-pub_date').select_related('author')
    is_followed = False
    if hasattr(request.user, 'follower_set') and request.user.follower_set.filter(followed=profile_user).exists():
        is_followed = True
    paged_posts = get_paged_posts(request, profile_user_posts)
    return render(request, 'blog/timeline.html',
                  {'posts': paged_posts, 'profile_user': profile_user, 'followed': is_followed})


@login_required
def toggle_following(request, username):
    followed = get_object_or_404(User, username=username)
    relationship = Follower.objects.filter(follower=request.user, followed=followed)
    if relationship.exists():
        relationship.delete()
    else:
        request.user.follower_set.create(followed=followed)
    return redirect('user_timeline', username=username)


class Login(View):
    def captcha(self, recaptcha_response):
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        return r.json()

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('my_timeline')
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            captcha_res = self.captcha(request.POST.get('g-recaptcha-response'))
            if not captcha_res['success']:
                messages.error(request, "Invalid reCaptcha. Please try again")
                return self.get(request)
            user = form.login()
            if user:
                login(request, user)
                return redirect('my_timeline')
        return self.get(request)


class Register(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('my_timeline')
        form = UserForm()
        return render(request, 'blog/register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You were successfully registered and can login now')
            return redirect('login_view')
        return self.get(request)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You were logger out')
    return redirect('public_timeline')
