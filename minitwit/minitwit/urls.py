
from django.conf.urls import include, url
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^$', views.MyTimeline.as_view(), name='timeline'),
    url(r'public/', views.public_timeline, name='public_timeline'),
    url(r'^user/(?P<username>\w+)/toggle/', views.toggle_following, name='toggle'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user/(?P<username>\w+)/', views.user_timeline, name='user_timeline'),
    url(r'^admin/', include(admin.site.urls)),
]
