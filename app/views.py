from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth import authenticate
from django.http import HttpResponse

from .models import StripeUser
from .forms import RegisterUser, LoginUser

import webapp.settings as settings
from decimal import Decimal
import json

# Create your views here.
def detail(request):
    try:
        user = StripeUser.objects.get(pk=request.session['user_id'])
    except:
        return redirect('app:login')
    return render(request, 'user/detail.html', {'user': user})

class CaptureStripeView(View):
    def post(self, request):
        event_json = json.loads(request.body.decode('utf-8'))
        try:
            user = StripeUser.objects.get(stripe_id=event_json['data']['object']['customer'])
        except:
            return redirect('app:login')
        user.payment_set.create(amount=Decimal(event_json['data']['object']['amount'])/100)
        return HttpResponse(status=200)

class SubscriptionStripeView(View):
    def get(self, request):
        return render(request, 'user/subscription.html')

    def post(self, request):
        try:
            user = StripeUser.objects.get(pk=request.session['user_id'])
        except:
            return redirect('app:login')
        if not user.stripe_id:
            return redirect('app:stripe')
        else:
            user.subscribe(request.POST['suscription_plan'])
            return redirect('app:detail')

class CardStripeView(View):
    def get(self, request):
        return render(request, 'user/stripe.html', {'publishable': settings.STRIPE_PUBLISHABLE})

    def post(self, request):
        try:
            user = StripeUser.objects.get(pk=request.session['user_id'])
        except:
            return redirect('app:login')
        user.create_account(request.POST['stripe_token'])
        return redirect('app:detail')

class RegisterView(View):
    def post(self, request):
        form = RegisterUser(request.POST)
        if form.is_valid():
            new_user = form.save()
            request.session['user_id'] = new_user.pk
            new_user.set_password(request.POST['password'])
            new_user.save()
            return redirect('app:detail')
        else:
            return render(request, 'user/register.html', { 'form': form })

    def get(self, request):
        form = RegisterUser()
        return render(request, 'user/register.html', { 'form': form })

class LoginView(View):
    def post(self, request):
        form = LoginUser(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            request.session['user_id'] = user.pk
            return redirect('app:detail')
        else:
            form.add_error(None, 'Incorrect username or password')
            return render(request, 'user/login.html', { 'form': form })

    def get(self, request):
        form = LoginUser()
        return render(request, 'user/login.html', { 'form': form })

class LogoutView(View):
    def post(self, request):
        request.session['user_id'] = None
        return redirect('app:login')
