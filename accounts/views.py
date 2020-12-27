from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate
# Create your views here.

def home(request):
    if request.user.is_authenticated:

        return render(request,'base.html')
    else:
        return HttpResponse('<center><h1>Please Login First</h1><center>')