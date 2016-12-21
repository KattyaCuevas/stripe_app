from decimal import Decimal
import json

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import webapp.settings as settings
from .models import StripeUser
from .forms import RegisterUser, LoginUser


class UserDetailView(LoginRequiredMixin, View):
    """
    Show detail of user profile
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'user/detail.html', {'user': request.user})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    """
    Get json of stripe webhook when charge is succeeded
    """
    def post(self, request):
        event_json = json.loads(request.body.decode('utf-8'))
        user = StripeUser.objects.get(stripe_id=event_json['data']['object']['customer'])
        user.payment_set.create(amount=Decimal(event_json['data']['object']['amount'])/100)
        return HttpResponse(status=200)


class StripeSubscriptionView(LoginRequiredMixin, View):
    """
    Get json of stripe webhook when charge is succeeded
    """
    login_url = '/login/'
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
    """
    Create new stripe token based on a card data
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'user/stripe.html', {'publishable': settings.STRIPE_PUBLISHABLE})

    def post(self, request):
        request.user.create_account(request.POST['stripe_token'])
        return redirect('app:detail')


class UserSignupView(View):
    """
    Create new user
    """
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
    """
    Sign in for an existent user
    """
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
