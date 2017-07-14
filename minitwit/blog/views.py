from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

from .models import Follower, Message
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


def timeline(request):
    if not request.user.is_authenticated():
        return public_timeline(request)
    followed_users = request.user.follower_set.values_list('followed', flat=True)
    all_ids = list(followed_users) + [request.user]
    posts = Message.objects.filter(author__in=all_ids).order_by('-pub_date')
    paged_posts = get_paged_posts(request, posts)
    return render(request, 'timeline.html', {'posts': paged_posts})


def public_timeline(request):
    latest_posts = Message.objects.order_by('-pub_date')
    paged_posts = get_paged_posts(request, latest_posts)
    return render(request, 'timeline.html', {'posts': paged_posts})


def user_timeline(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile_user_posts = profile_user.message_set.order_by('-pub_date')
    is_followed, is_same_user = False, False
    if request.user.is_authenticated():
        current_user_id = request.user.pk
        if request.user.follower_set.filter(followed=profile_user).exists():
            is_followed = True
        if profile_user.pk == current_user_id:
            is_same_user = True
    paged_posts = get_paged_posts(request, profile_user_posts)
    return render(request, 'timeline.html',
                  {'posts': paged_posts, 'profile_user': profile_user, 'followed': is_followed,
                   'same_user': is_same_user})


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


@login_required
def add_message(request):
    if request.POST.get('text'):
        request.user.message_set.create(text=request.POST.get('text'))
    return redirect('timeline')


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
