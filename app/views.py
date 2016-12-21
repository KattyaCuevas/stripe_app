from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .models import StripeUser
from .forms import RegisterUser, LoginUser

import webapp.settings as settings
from decimal import Decimal
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class UserDetailView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'user/detail.html', {'user': request.user})

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request):
        event_json = json.loads(request.body.decode('utf-8'))
        user = StripeUser.objects.get(stripe_id=event_json['data']['object']['customer'])
        user.payment_set.create(amount=Decimal(event_json['data']['object']['amount'])/100)
        return HttpResponse(status=200)

class StripeSubscriptionView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'user/subscription.html')

    def post(self, request):
        user = request.user
        if not user.stripe_id:
            return redirect('app:stripe')
        else:
            user.subscribe(request.POST['suscription_plan'])
            return redirect('app:detail')

class StripeCardView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'user/stripe.html', {'publishable': settings.STRIPE_PUBLISHABLE})

    def post(self, request):
        try:
            user = StripeUser.objects.get(pk=request.session['user_id'])
        except:
            return redirect('app:login')
        user.create_account(request.POST['stripe_token'])
        return redirect('app:detail')

class UserSignupView(View):
    def post(self, request):
        form = RegisterUser(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(request.POST['password'])
            new_user.save()
            login(request, new_user)
            return redirect('app:detail')
        else:
            return render(request, 'user/register.html', { 'form': form })

    def get(self, request):
        form = RegisterUser()
        return render(request, 'user/register.html', { 'form': form })

class UserSigninView(View):
    def post(self, request):
        form = LoginUser(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('app:detail')
        else:
            form.add_error(None, 'Nombre de usuario o contraseña incorrecta')
            return render(request, 'user/login.html', { 'form': form })

    def get(self, request):
        form = LoginUser()
        return render(request, 'user/login.html', { 'form': form })

class UserSignoutView(View):
    def post(self, request):
        logout(request)
        return redirect('app:login')
