from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^compare/$', views.compare, name='compare'),
]
