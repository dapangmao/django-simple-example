from django.conf.urls import url
from . import views


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.timeline, name='timeline'),
    url(r'public/', views.public_timeline, name='public_timeline'),
    url(r'^user/(?P<username>\w+)/unfollow/', views.unfollow_user, name='unfollow_user'),
    url(r'^user/(?P<username>\w+)/follow/', views.follow_user, name='follow_user'),
    url(r'^add_message/$', views.add_message, name='add_message'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user/(?P<username>\w+)/', views.user_timeline, name='user_timeline'),
]