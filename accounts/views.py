from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from keras_vggface.utils import preprocess_input
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages
from .models import Employee,EmployeeFaceData,EmployeeProfile
import numpy as np
import cv2
import os
import io

#rest_framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import EmployeeFaceDataSerializer,EmployeeSerializer,EmployeeProfileSerializer

# Create your views here.

"""Helper functions and loading importing keras model instance from settings"""
model = settings.MODEL
graph = settings.GRAPH
cascade = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'accounts/haarcascade_frontalface_alt.xml'))

def preprocess_image(image):
    image = cv2.resize(image,(224,224))
    image = np.asarray(image,'float64')
    image = image.reshape(1,224,224,3)
    image = preprocess_input(image,version=2)
    return image

def get_embedding(image,model=model,graph=graph):
    image = preprocess_image(image)
    try:
        with graph.as_default():
            yhat = model.predict(image)
        yhat = yhat.reshape(2048)
        yhat = list(yhat)
    except:
        yhat = None
    return yhat

def capture_face():
    #opens the attatched web-camera to capture face embeddings
    #returns embeddings ( 2048 element vector encoded in BytesIO,datatype of array is float32 )
        cap = cv2.VideoCapture(0)
        while True:
            ret,frame = cap.read()
            faces = cascade.detectMultiScale(frame)
            if len(faces)>0:
                for x,y,w,h in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
            cv2.imshow('camera',frame)
            if cv2.waitKey(1)==ord('q'):
                if len(faces)>0:
                    face_img = frame[y:y+h,x:x+w]
                    yhat = get_embedding(face_img)
                    break
                else:
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
                    messages.success(request,'employee successfully added')
                else:
                    empface = EmployeeFaceData(employee=emp[0],embeddings=yhat)
                    empface.save()
                    messages.success(request,'face data captured')
                return redirect('dashboard')
    else:
        raise PermissionDenied

    return render(request,'register.html')


# api_views below
@api_view(['GET'])
def employeeFaceApi(request):
    empface = EmployeeFaceData.objects.all()
    serializer = EmployeeFaceDataSerializer(empface,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def employeeApi(request):
    emp = Employee.objects.all()
    serializer = EmployeeSerializer(emp,many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def employeeProfileApi(request):
    emppro = EmployeeProfile.objects.all()
    serializer = EmployeeProfileSerializer(emppro,many=True)
    return Response(serializer.data)