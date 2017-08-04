from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^$', views.MyTimeline.as_view(), name='my_timeline'),
    url(r'public/', views.public_timeline, name='public_timeline'),
    url(r'^user/(?P<username>\w+)/toggle/', views.toggle_following, name='toggle'),
    url(r'^user/(?P<username>\w+)/', views.user_timeline, name='user_timeline'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),

    # url(r'^logout/$', views.logout_view, name='logout_view'),
    # url(r'^login/$', views.Login.as_view(), name='login_view'),
    # url(r'^register/$', views.Register.as_view(), name='register'),

]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
