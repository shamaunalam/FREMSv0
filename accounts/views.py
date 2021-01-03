from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import Employee
import cv2
# Create your views here.

def Dashboard(request):

    if request.user.is_authenticated:
        full_name = request.user.full_name
        if request.user.is_staff:
            return render(request,'admindash.html',{'full_name':full_name})
        else:
            return render(request,'employeedash.html',{'full_name':full_name})
    else:
        return redirect('login')

def Login(request):
    #renders the login page if get request
    #on post request submits the login form
    # and logs in the user 
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
    #logs out the current user, by calling 
    #django.contrib.auth logout(request)
    #redirects to Login view.

    if request.user is not None:
        logout(request)
        return redirect('login')

@login_required(login_url='login')
def Register(request):
    if request.user.is_staff:
        if request.method=="POST":
            capture_face(request)
            EmpId,full_name,password_1,password_2 = request.POST['EmpId'],request.POST['full_name'],request.POST['password_1'],request.POST['password_2']
            if password_1==password_2:
                emp = Employee.objects.filter(EmpId=EmpId)
                if not emp:
                    emp = Employee.objects.create_user(EmpId,full_name,password_2)
                    emp.save()
                return redirect('dashboard')
    else:
        raise PermissionDenied

    return render(request,'register.html')

@login_required(login_url='login')
def capture_face(request):
    if request.user.is_staff:
        cap = cv2.VideoCapture(0)

        while True:

            ret,frame = cap.read()

            cv2.imshow('camera',frame)

            if cv2.waitKey(1)==ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    return redirect('dashboard')