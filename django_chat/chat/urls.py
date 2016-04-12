from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'channels/$', views.ChannelView.as_view(), name='channel-list'),
    url(r'channels/(?P<pk>\d+)/$',
        views.ChannelView.as_view(), name='channel-detail'),
    url(r'^channels/(?P<pk>\d+)/messages/$',
        views.message_list, name='message-list'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^logged/$', views.logged_view, name='logged'),
]
