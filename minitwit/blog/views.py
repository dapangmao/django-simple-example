from werkzeug import check_password_hash, generate_password_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import User, Follower, Message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# TODO: separate form
# TODO: enhance admin
# TODO: explore absolute redirect

def base_timeline(request, posts):
    paginator = Paginator(posts, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        paged_posts = paginator.page(page)
    except PageNotAnInteger:
        paged_posts = paginator.page(1)
    except EmptyPage:
        paged_posts = paginator.page(paginator.num_pages)
    return render(request, 'timeline.html', {'posts': paged_posts})


def timeline(request):
    try:
        current_user_id = request.session['user_id']
    except KeyError:
        return redirect('public_timeline')
    current_user = User.objects.get(pk=current_user_id)
    following_ids = current_user.follower_set.values_list('whom', flat=True)
    all_ids = list(following_ids) + [current_user_id]
    posts = Message.objects.filter(author_id__in=all_ids).order_by('-pub_date')
    return base_timeline(request, posts)


def public_timeline(request):
    latest_posts = Message.objects.order_by('-pub_date')
    return base_timeline(request, latest_posts)


def user_timeline(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponse('This user does not exist', status=401)
    posts = profile_user.message_set.order_by('-pub_date')[:20]
    current_user_id = request.session.get('user_id')
    is_followed = False
    if current_user_id and User.objects.get(pk=current_user_id).follower_set.filter(whom=profile_user.pk).exists():
        is_followed = True
    is_same_user = False
    if current_user_id and profile_user.pk == current_user_id:
        is_same_user = True
    return render(request, 'timeline.html', {'posts': posts, 'profile_user': profile_user, 'followed': is_followed,
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
    error = None
    if request.method == 'POST':
        current_username = request.POST.get('username')
        current_password = request.POST.get('password')
        current_password2 = request.POST.get('password2')
        current_email = request.POST.get('email')
        if current_username is None:
            error = 'You have to enter a username'
        elif current_email is None or '@' not in current_email:
            error = 'You have to enter a valid email address'
        elif current_password is None:
            error = 'You have to enter a password'
        elif current_password != current_password2:
            error = 'The two passwords do not match'
        elif User.objects.filter(username=current_username).exists():
            error = 'The username is already taken'
        else:
            current_user = User(username=current_username, email=current_email,
                                pw_hash=generate_password_hash(current_password))
            current_user.save()
            messages.success(request, 'You were successfully registered and can login now')
            return redirect('login')
    return render(request, 'register.html', {'error': error})


def logout(request):
    request.session.pop('user_id')
    request.session.pop('username')
    messages.success(request, 'You were logger out')
    return redirect('public_timeline')







