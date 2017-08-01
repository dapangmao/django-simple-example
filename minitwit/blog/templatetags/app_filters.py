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