from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def Dashboard(request):

    if request.user.is_authenticated:
        return render(request,'base.html')
    else:
        return redirect('login')

def Login(request):
    if request.method == 'POST':
        EmpId = request.POST['EmpId']
        password = request.POST['password']

        user = authenticate(request,EmpId=EmpId,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request,'login.html')

def Logout(request):
    if request.user is not None:
        logout(request)
        return redirect('login')