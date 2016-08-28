from hashlib import md5
from werkzeug import check_password_hash, generate_password_hash
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse
from .models import User, Follower, Message
import time
from datetime import datetime
# Create your views here.


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')



def timeline(request):
    if not request.session['user_id']:
        return redirect('public_timeline')
    user_id = request.session['user_id']
    following_ids = Follower.objects.filter(who=user_id).values_list('whom', flat=True)
    all_ids = following_ids + [user_id]
    posts = Message.objects.filter(author__in=all_ids).order_by('-pub_date')[:20].select_related('user__username')
    return render(request, 'timeline.html', {'posts': posts})


def public_timeline(request):
    latest_posts = Message.objects.order_by('-pub_date')[:20].select_related('user__username')
    return render(request, 'timeline.html', {'latest_posts': latest_posts})



def user_timeline(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_followed = False
    if request.session['user_id']:
        is_followed = Follower.filter(who=request.session['user_id'], whom=profile_user[0].pk).exists()
    posts = Message.objects.filter(author=profile_user.pk).order_by('-pub_date')[:20]
    # change the messages both here and the templates to posts
    return render(request, 'timeline.html', {'posts': posts, 'profile_user': profile_user, 'followed': is_followed})


def follow_user(request, username):
    if not request.session['user_id']:
        return HttpResponse('Unauthorized', status=401)
    whom_queryset = User.objects.filter(username=username)
    if not whom_queryset.exists():
        return HttpResponse('No such a user', status=404)
    current = Follower(who=request.session['user_id'], whom=whom_queryset[0].pk)
    current.save()
    return redirect('user_timeline', username=username) # http://stackoverflow.com/questions/13328810/django-redirect-to-view


def unfollow_user(request, username):
    if not request.session['user_id']:
        return HttpResponse('Unauthorized', status=401)
    whom_queryset = User.objects.filter(username=username)
    if not whom_queryset.exists():
        return HttpResponse('No such a user', status=404)
    current = Follower.filter(who=request.session['user_id'], whom=whom_queryset[0].pk)
    current.delete()
    return redirect('user_timeline', username=username)


def add_message(request):
    if not request.session['user_id']:
        return HttpResponse('Unauthorized', status=401)
    if request.POST.get('text'):
        current = Message(author=request.session['user_id'], text=request.POST.get('text'), pub_date=time.time())
        current.save()
    return redirect('timeline')


def login(request):
    """Logs the user in."""
    if request.session['user_id']:
        return redirect('timeline')
    error = None
    if request.method == 'POST':
        current_username = request.POST.get('username')
        current_password = request.POST.get('possword')
        user = User.objects.filter(username=current_username)[0]
        if not user.exists():
            error = 'Invalid username'
        elif not check_password_hash(user.pw_hash, current_password):
            error = 'Invalid password'
        else:
            # flash('You were logged in')
            request.session['user_id'] = user.pk
            return redirect('timeline')
    return render(request, 'login.html', {'error': error})



def register(request):
    if request.session['user_id']:
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
            # flash('You were successfully registered and can login now')
            return redirect('login')
    return render(request, 'register.html', {'error': error})



def logout(request):
    # flash('You were logged out')
    request.session.pop('user_id')
    return redirect('public_timeline')







