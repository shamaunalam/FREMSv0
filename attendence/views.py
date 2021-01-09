from django.shortcuts import render,redirect
from accounts.views import preprocess_image,get_embedding,capture_face
from accounts.models import EmployeeFaceData
import cv2
import numpy as np
from scipy.spatial.distance import cosine 
from django.conf import settings
import os
# Create your views here

model = settings.MODEL
graph = settings.GRAPH
cascade = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'accounts/haarcascade_frontalface_alt.xml'))

def convert_to_array(yhat):
    arr = np.array(yhat).reshape(1,2048)
    return arr

def fetch_all_employees_face():
    all_emp = EmployeeFaceData.objects.all()
    if all_emp is not None:
            emp_id = [emp.employee.EmpId for emp in all_emp]
            emp_embeddings = [convert_to_array(emp.embeddings) for emp in all_emp]
            return emp_id,emp_embeddings
    else:
            return None
                

def mark_attendence(request):
    
    emp_id,emp_embeddings = fetch_all_employees_face()
    yhat_new = capture_face()
    yhat_new = convert_to_array(yhat_new)
    for i,emb in enumerate(emp_embeddings):
        print(i,emb.shape)
        print(cosine(yhat_new,emb))
    return redirect('dashboard')
            


