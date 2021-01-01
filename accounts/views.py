from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import PermissionDenied
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
        if EmpId and password:
            user = authenticate(request,EmpId=EmpId,password=password)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
        else:
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request,'login.html')

def Logout(request):
    if request.user is not None:
        logout(request)
        return redirect('login')

def Register(request):
    if not request.user.is_staff:
        raise PermissionDenied
    return render(request,'register.html')