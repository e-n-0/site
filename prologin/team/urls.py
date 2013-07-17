from django.conf.urls import patterns, url
from team import views

urlpatterns = patterns('',
    url(r'^$', views.redir, name='index'),
    url(r'^(?P<year>\d+)/$', views.index, name='year'),
)
