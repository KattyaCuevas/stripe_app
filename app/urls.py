from django.conf.urls import url
from . import views
from .views import LoginView, RegisterView, LogoutView

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login', LoginView.as_view(), name='login'),
    url(r'logout', LogoutView.as_view(), name='logout'),
    url(r'me', views.detail, name='detail'),
    url(r'register', RegisterView.as_view(), name='register'),
]
