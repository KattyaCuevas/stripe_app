from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from .models import StripeUser
from .forms import RegisterUser

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
            return redirect('app:detail', user_id=new_user.pk)
    else:
        form = RegisterUser()

    return render(request, 'user/register.html', { 'form': form })
