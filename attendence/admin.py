from django.contrib import admin
from .models import EmployeeAttendence
# Register your models here.
class EmployeeAttendenceConfig(admin.ModelAdmin):

    search_fields = ("EmpId",'date')
    model = EmployeeAttendence
    ordering = ('-date',)
    list_display = ('date','get_eid','get_name','in_datetime','out_datetime','duration','status')
    
    def get_eid(self,obj):
        return obj.employee.EmpId

    def get_name(self,obj):
        return obj.employee.full_name
    get_eid.short_description = 'Person Number'  #Renames column head
    get_name.short_description = 'Person Name'

admin.site.register(EmployeeAttendence,EmployeeAttendenceConfig)