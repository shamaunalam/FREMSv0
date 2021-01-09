from django.urls import path
from . import views

urlpatterns = [
    path('mark',views.mark_attendence,name='mark'),
]