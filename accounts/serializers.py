from rest_framework import serializers
from .models import Employee,EmployeeProfile,EmployeeFaceData


class EmployeeFaceDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeFaceData
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = '__all__'