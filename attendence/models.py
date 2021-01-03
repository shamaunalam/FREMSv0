from django.db import models
from accounts.models import Employee
# Create your models here.
class EmployeeAttendence(models.Model):

    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    date = models.DateField()
    in_datetime = models.DateTimeField(blank=True,null=True)
    out_datetime = models.DateTimeField(blank=True,null=True)
    duration = models.DurationField(null=True,blank=True)
    status = models.CharField(max_length=10,choices=(('A','Absent'),('P','Present'),('HF','Half Day'),('L','Leave')))

    def get_duration(self):
        
        if self.in_datetime and self.out_datetime:

            tdlta = self.out_datetime - self.in_datetime
            return tdlta

    def __str__(self):
        return self.employee.EmpId