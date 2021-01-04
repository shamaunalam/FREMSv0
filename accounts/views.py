from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from keras_vggface.utils import preprocess_input
from django.shortcuts import render,redirect
from django.conf import settings
from .models import Employee,EmployeeFaceData
import numpy as np
import cv2
import os
import io
# Create your views here.

"""Helper functions and loading importing keras model instance from settings"""
model = settings.MODEL
graph = settings.GRAPH
cascade = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'accounts/haarcascade_frontalface_alt.xml'))
def capture_face():
        cap = cv2.VideoCapture(0)
        while True:

            ret,frame = cap.read()

            faces = cascade.detectMultiScale(frame)

            for x,y,w,h in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)

            cv2.imshow('camera',frame)

            if cv2.waitKey(1)==ord('q'):
                face_img = frame[y:y+h,x:x+w]
                face_img = cv2.resize(face_img,(224,224))
                face_img = np.asarray(face_img,'float64')
                face_img = face_img.reshape(1,224,224,3)
                face_img = preprocess_input(face_img,version=2)
                with graph.as_default():
                    yhat = model.predict(face_img)
                yhat = io.BytesIO(yhat)
                yhat = yhat.getvalue()
                break
        cap.release()
        cv2.destroyAllWindows()
        return yhat

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
            yhat  = capture_face()
            EmpId,full_name,password_1,password_2 = request.POST['EmpId'],request.POST['full_name'],request.POST['password_1'],request.POST['password_2']
            if password_1==password_2:
                emp = Employee.objects.filter(EmpId=EmpId)
                if not emp:
                    emp = Employee.objects.create_user(EmpId,full_name,password_2)
                    emp.save()
                    empface = EmployeeFaceData(employee=emp,embeddings=yhat)
                    empface.save()
                else:
                    empface = EmployeeFaceData(employee=emp[0],embeddings=yhat)
                    empface.save()
                    print('face captured')
                return redirect('dashboard')
    else:
        raise PermissionDenied

    return render(request,'register.html')

