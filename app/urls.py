from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='login', permanent=False), name='root'),
    url(r'^login/$', UserSigninView.as_view(), name='login'),
    url(r'^logout/$', UserSignoutView.as_view(), name='logout'),
    url(r'^me/$', UserDetailView.as_view(), name='detail'),
    url(r'^register/$', UserSignupView.as_view(), name='register'),
    url(r'^stripe/$', StripeCardView.as_view(), name='stripe'),
    url(r'^subscription/$', StripeSubscriptionView.as_view(), name='subscription'),
    url(r'^capture/$', StripeWebhookView.as_view(), name='capture'),
]
