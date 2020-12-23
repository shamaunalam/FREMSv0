from django.contrib import admin
from .models import Employee
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput,Textarea
# Register your models here.


class UserAdminConfig(UserAdmin):

    model = Employee
    search_fields = ('EmpId',
    'full_name')
    list_filter = ('EmpId',
    'full_name','is_active','is_staff')
    ordering = ('-date_joined',)
    list_display = ('EmpId',
    'full_name','is_active','is_staff')
    fieldsets = (
        (None,{'fields':('EmpId','full_name','phone_number','post_title')}),
        ('Permissions',{'fields':('is_staff','is_active','is_superuser','groups')}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('EmpId','full_name','phone_number','password1','password2','is_active','is_staff')}),
            )

admin.site.register(Employee,UserAdminConfig)