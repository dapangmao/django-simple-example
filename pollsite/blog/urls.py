from django.conf.urls import url
from . import views

# TODO: django's re for url routing

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.timeline, name='timeline'),
    url(r'^public$', views.public_timeline, name='public_timeline'),
    # # ex: /polls/5/results/
    url(r'^(?P<username>)/$', views.user_timeline, name='user_timeline'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]