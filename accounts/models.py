from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
# Create your models here.

class EmployeeManager(BaseUserManager):


    def create_superuser(self,EmpId,full_name,password,**other_fields):

        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(EmpId,full_name,password,**other_fields)


    def create_user(self,EmpId,full_name,password,**other_fields):
        if not EmpId:
            raise ValueError(_("You must provide an employee Id"))

        user = self.model(EmpId=EmpId,full_name=full_name,**other_fields)
        user.set_password(password)
        user.save()
        return user 

class Employee(AbstractBaseUser,PermissionsMixin):

    EmpId = models.CharField(max_length=10,unique=True)
    full_name = models.CharField(max_length=150,blank=False)
    phone_number = models.CharField(max_length=15)
    post_title = models.CharField(max_length=50,choices=[('Executive','Executive'),('Sr. Manager','Sr. Manager'),('Manager','Manager'),('Sr. Engineer','Sr. Engineer'),('Engineer','Engineer'),('Master Craftsman','Master Craftsman'),('Admin staff','Admin staff'),('placement cell','placement cell'),('GET','Graduate Engineer Trainee'),('OJT','On Job Trainee')])
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = EmployeeManager()
    USERNAME_FIELD = 'EmpId'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

    