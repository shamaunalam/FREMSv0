from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
# Create your models here.

class EmployeeManager(BaseUserManager):

    """
    Custom User Manager for the user class Employee.
    methods : 
    create_superuser :- used by the manage.py createsuperuser command
    create_user :- the default user creation method is_admin=false,is_staff=false,is_active=true
    ,additional arguments can be passed
    """
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
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = EmployeeManager()
    USERNAME_FIELD = 'EmpId'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

"""
class EmployeeProfile(models.Model):


    The Profile model, non_auth realted information about employee, recieves
    post_save and pre_save signals to create default profile for every employee created
   

    emp = models.OneToOneField(Employee,on_delete=models.CASCADE,primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name =  models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(_('email'),balnk=True,null=True)
    designation = models.CharField(max_length=50,choices=(('EXE','Executive'),('SR_MGR','Senior manager'),('MGR','Manager'),('SR_ENG','Senior Engineer'),('ENG','Engineer'),('MCM','Master Craftsman'),('GET','Graduate Engineer Trainee'),('DET','Diploma Engineer Trainee'),('OJT','On Job Trainee')))
    section = models.CharField(max_length=10,choices=[('ADM','Administration'),('PRO','Production'),('TRG','Training')])
    department = models.CharField(max_length=20,blank=True)
    photo = models.ImageField()
    face_data = ArrayField(base_field=models.BinaryField(),blank=True)

"""

