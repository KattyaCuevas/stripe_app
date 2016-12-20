from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'app'
urlpatterns = [
    url(r'login', LoginView.as_view(), name='login'),
    url(r'logout', LogoutView.as_view(), name='logout'),
    url(r'me', DetailView.as_view(), name='detail'),
    url(r'register', RegisterView.as_view(), name='register'),
    url(r'stripe', CardStripeView.as_view(), name='stripe'),
    url(r'subscription', SubscriptionStripeView.as_view(), name='subscription'),
    url(r'capture', csrf_exempt(CaptureStripeView.as_view()), name='capture'),
]
