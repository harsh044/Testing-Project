import json
from rest_framework import serializers
from apps.teacher.models import Account,Student
from django.core.validators import RegexValidator,EmailValidator
from django.conf import settings
from common import utils

class TeacherAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','mobile','address','department','experience']
    
class CreateRegisterSerializer(serializers.Serializer):
    first_name =  serializers.CharField(max_length=50)
    last_name =  serializers.CharField(max_length=50)
    email =  serializers.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'[0-9]{10,15}', message="Invalid phone nnumber")
    mobile =  serializers.CharField(max_length=50,validators=[phone_regex])
    address =  serializers.CharField(max_length=100)
    dob =  serializers.DateField()
    gender = serializers.CharField(max_length=50)
    experience =  serializers.IntegerField()
    department =  serializers.IntegerField()
    password_regex = RegexValidator(
        regex=r'[A-Za-z0-9]', message="Invalid Password.")
    password =  serializers.CharField(min_length=8,max_length=10,validators=[password_regex])
        
    def validation(self,data):
        if int(data['department']) not in settings.DEPARTMENT:
            return 108
        return data

class CreateLoginSerializer(serializers.Serializer):
    username =  serializers.CharField(max_length=50,required=True)
    password =  serializers.CharField(max_length=50,required=True)
    
class UpdateProfileSerializer(serializers.Serializer):
    first_name =  serializers.CharField(max_length=50)
    last_name =  serializers.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'[0-9]{10,15}', message="Invalid phone nnumber")
    mobile =  serializers.CharField(max_length=50,validators=[phone_regex])
    address =  serializers.CharField(max_length=100)
    dob = serializers.DateField()
    gender = serializers.CharField(max_length=2)
    experience =  serializers.IntegerField()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name','last_name','email','mobile','department','address','rollno','dob','gender']
        
class StudentlistSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    rollno = serializers.SerializerMethodField()
            
    class Meta:
        model = Account
        fields = ['first_name','last_name','rollno','email','mobile','department','address','dob','gender','teacher']
        
    def get_teacher(self,obj):
        teacher_obj = Account.objects.filter(id=obj.created_by).last()
        teacher = TeacherAuthSerializer(teacher_obj)
        return teacher.data
    
    def get_rollno(self,obj):
        rollno_obj =  Student.objects.filter(id=obj.id).last()
        return rollno_obj.rollno

class CreateStudentSerializer(serializers.Serializer):
    first_name =  serializers.CharField(max_length=50)
    last_name =  serializers.CharField(max_length=50)
    email =  serializers.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'[0-9]{10,15}', message="Invalid phone nnumber")
    mobile =  serializers.CharField(max_length=50,validators=[phone_regex])
    address =  serializers.CharField(max_length=100)
    rollno = serializers.IntegerField()
    dob = serializers.DateField()
    gender = serializers.CharField(max_length=1)
    
class UpdateStudentSerializer(serializers.Serializer):
    first_name =  serializers.CharField(max_length=50)
    last_name =  serializers.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'[0-9]{10,15}', message="Invalid phone nnumber")
    mobile =  serializers.CharField(max_length=50,validators=[phone_regex])
    address =  serializers.CharField(max_length=100)
    rollno = serializers.IntegerField()
    dob = serializers.DateField()
    gender = serializers.CharField(max_length=1)