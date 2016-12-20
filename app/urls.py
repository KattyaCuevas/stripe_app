from django.conf.urls import url
from . import views
from .views import LoginView, RegisterView

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register', RegisterView.as_view(), name='register'),
    url(r'login', LoginView.as_view(), name='login'),
    url(r'me', views.detail, name='detail'),
]
