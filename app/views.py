from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth import authenticate

from .models import StripeUser
from .forms import RegisterUser, LoginUser

# Create your views here.
def index(request):
    return render(request, 'user/index.html')

def detail(request):
    try:
        user = StripeUser.objects.get(pk=request.session['user_id'])
    except:
        return redirect('app:login')
    return render(request, 'user/detail.html', {'user': user})

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
