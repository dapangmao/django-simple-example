from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Follower, Message
from .forms import UserForm
from werkzeug import check_password_hash


# TODO: enhance admin
# TODO: explore absolute redirect

def get_paged_posts(request, posts, n=5):
    paginator = Paginator(posts, n) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        paged_posts = paginator.page(page)
    except PageNotAnInteger:
        paged_posts = paginator.page(1)
    except EmptyPage:
        paged_posts = paginator.page(paginator.num_pages)
    return paged_posts


def timeline(request):
    try:
        current_user_id = request.session['user_id']
    except KeyError:
        return redirect('public_timeline')
    current_user = User.objects.get(pk=current_user_id)
    following_ids = current_user.follower_set.values_list('whom', flat=True)
    all_ids = list(following_ids) + [current_user_id]
    posts = Message.objects.filter(author_id__in=all_ids).order_by('-pub_date')
    paged_posts = get_paged_posts(request, posts)
    return render(request, 'timeline.html', {'posts': paged_posts})


def public_timeline(request):
    latest_posts = Message.objects.order_by('-pub_date')
    paged_posts = get_paged_posts(request, latest_posts)
    return render(request, 'timeline.html', {'posts': paged_posts})


def user_timeline(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponse('This user does not exist', status=401)
    profile_user_posts = profile_user.message_set.order_by('-pub_date')
    current_user_id = request.session.get('user_id')
    is_followed = False
    if current_user_id and User.objects.get(pk=current_user_id).follower_set.filter(whom=profile_user.pk).exists():
        is_followed = True
    is_same_user = False
    if current_user_id and profile_user.pk == current_user_id:
        is_same_user = True
    paged_posts = get_paged_posts(request, profile_user_posts)
    return render(request, 'timeline.html', {'posts': paged_posts, 'profile_user': profile_user, 'followed': is_followed,
                                             'same_user': is_same_user})


def follow_user(request, username):
    try:
        current_user_id = request.session['user_id']
    except KeyError:
        return HttpResponse('Unauthorized', status=401)
    try:
        whom_pk = User.objects.get(username=username).pk
    except ObjectDoesNotExist:
        return HttpResponse('This user does not exist', status=404)
    User.objects.get(pk=current_user_id).follower_set.create(whom=whom_pk)
    return redirect('user_timeline', username=username)


def unfollow_user(request, username):
    try:
        current_user_id = request.session['user_id']
    except KeyError:
        return HttpResponse('Unauthorized', status=401)
    try:
        whom_pk = User.objects.get(username=username).pk
    except ObjectDoesNotExist:
        return HttpResponse('This user does not exist', status=404)
    Follower.objects.filter(who_id=current_user_id, whom=whom_pk).delete()
    return redirect('user_timeline', username=username)


def add_message(request):
    if 'user_id' not in request.session:
        return HttpResponse('Unauthorized', status=401)
    if request.POST.get('text'):
        current_user = User.objects.get(pk=request.session['user_id'])
        current_user.message_set.create(author=request.session['user_id'], text=request.POST.get('text'),
                                        pub_date=datetime.utcnow())
    return redirect('timeline')


def login(request):
    """Logs the user in."""
    if 'user_id' in request.session:
        return redirect('timeline')
    error = None
    if request.method == 'POST':
        current_username = request.POST.get('username')
        current_password = request.POST.get('password')
        try:
            user = User.objects.get(username=current_username)
        except ObjectDoesNotExist:
            error = 'Not a valid user'
        else:
            if not check_password_hash(user.pw_hash, current_password):
                error = 'Invalid password'
            else:
                messages.success(request, 'You were logged in')
                request.session['user_id'] = user.pk
                request.session['username'] = user.username
                return redirect('timeline')
    return render(request, 'login.html', {'error': error})


def register(request):
    if 'user_id' in request.session:
        return redirect('timeline')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You were successfully registered and can login now')
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


def logout(request):
    request.session.pop('user_id')
    request.session.pop('username')
    messages.success(request, 'You were logger out')
    return redirect('public_timeline')
