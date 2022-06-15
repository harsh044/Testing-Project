# from dataclasses import fields
# from pyexpat import model
# import email
# from typing_extensions import Required
# from unittest.util import _MAX_LENGTH
# from pkg_resources import require
# from apps.employee import validators
from rest_framework import serializers
from apps.employee.models import Employee
from django.core.validators import RegexValidator,EmailValidator

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','first_name','last_name','email','city','designation','salary']

class UserDetailSerializeer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','first_name','last_name','email','username','city','designation','salary']
        
        
class CreateEmployeeSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(max_length=100, required=True,validators=[EmailValidator])
    city = serializers.CharField(max_length=50, required=True)
    designation = serializers.CharField(max_length=50, required=True)
    salary = serializers.FloatField()
    
class EmployeeAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name','last_name','email','username','password']
    
class CreateRegisterSerializer(serializers.Serializer):
    first_name =  serializers.CharField(max_length=50)
    last_name =  serializers.CharField(max_length=50)
    email =  serializers.CharField(max_length=50)
    username =  serializers.CharField(max_length=50)
    password_regex = RegexValidator(
        regex=r'[A-Za-z0-9]', message="Invalid Password.")
    password =  serializers.CharField(max_length=10,validators=[password_regex])
    
class CreateLoginSerializer(serializers.Serializer):
    username =  serializers.CharField(max_length=50,required=True)
    password =  serializers.CharField(max_length=50,required=True)