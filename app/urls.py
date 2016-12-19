from django.conf.urls import url
from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register', views.register, name='register'),
    url(r'login', views.login, name='login'),
    url(r'^(?P<user_id>[0-9]+)/$', views.detail, name='detail'),
]
