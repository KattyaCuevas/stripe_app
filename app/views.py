from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth import authenticate

from .models import StripeUser
from .forms import RegisterUser, LoginUser

# Create your views here.
def index(request):
    return render(request, 'user/index.html')

def detail(request, user_id):
    user = get_object_or_404(StripeUser, pk=user_id)
    return render(request, 'user/detail.html', {'user': user})

def register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            new_user = form.save()
            request.session['user_id'] = new_user.pk
            new_user.set_password(request.POST['password'])
            new_user.save()
            return redirect('app:detail', user_id=new_user.pk)
    else:
        form = RegisterUser()

    return render(request, 'user/register.html', { 'form': form })

def login(request):
    if request.method == 'POST':
        form = LoginUser(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            return redirect('app:detail', user_id=user.pk)
        else:
            return render(request, 'user/login.html', { 'form': form })
    else:
        form = LoginUser()

    return render(request, 'user/login.html', { 'form': form })
