from hashlib import md5

from django.shortcuts import render
from .models import User, Follower, Message
# Create your views here.

def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)



def timeline(request):
    pass



def public_timeline(request):
    pass



def user_timeline(request, username):
    pass


def follow_user(request, username):
    pass


def add_message(request):
    pass


def login(request):
    pass


def register(request):
    pass


def logout(request):
    pass