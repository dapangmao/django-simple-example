from django.conf.urls import url
from . import views


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.timeline, name='timeline'),
    url(r'public/', views.public_timeline, name='public_timeline'),
    url(r'^(?P<username>\w+)/unfollow/', views.unfollow_user, name='unfollow_user'),
    url(r'^(?P<username>\w+)/follow/', views.follow_user, name='follow_user'),
    url(r'^add_message/$', views.add_message, name='add_message'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^(?P<username>\w+)/', views.user_timeline, name='user_timeline'),
]