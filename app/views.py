from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello.")
