
from dataclasses import dataclass
import json
from urllib import request
from django.conf import settings
from apps.teacher.models import Account
from api.teacher.serializer import TeacherAuthSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from django.db.models import Q
from apps.teacher.model_parser import extract_student_list_to_dict,extract_student_detail_to_dict

from apps.teacher.models import Student

def register(first_name,last_name,email,mobile,address,experience,dob,gender,password,department,user):
    check_if_email_exists = Account.objects.filter(email=email)
    if check_if_email_exists:
        return 101
    
    user_obj = Account.objects.create(
        first_name = first_name,
        last_name = last_name,
        email = email,
        mobile = mobile,
        is_hod = True,
        is_staff = True,
        address = address,
        experience = experience,
        dob = dob,
        gender = gender,
        username = email,
        password = password,
        department = department,
        created_by = user.id
    )
    if not user_obj:
        return 100
    
    group = Group.objects.filter(name="admin").last()
    user_obj.set_password(password)
    user_obj.groups.add(group)
    user_obj.save()
    
    return 201

def get_token_from_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def login(username,password):
    user_obj = Account.objects.filter(Q(is_hod=True) | Q(is_superuser=True),username=username).last()
    
    if not user_obj:
        return 105
    
    if not user_obj.check_password(password):
        return 106
    
    jwt_response = get_token_from_user(user_obj)
    if not jwt_response:
        return 100
    
    
    bearer_token = {key: f"{settings.AUTH_PREFIX} {val}" for key, val in jwt_response.items()}
    user_details = TeacherAuthSerializer(user_obj)
    return {
        "token" : bearer_token,
        "user_details" : user_details.data
    }
    
def createstudent(first_name,last_name,email,mobile,marks,address,rollno,dob,gender,teacher):
    check_if_email_exists = Account.objects.filter(email=email)
    if check_if_email_exists:
        return 101

    account_obj = Account.objects.create(
        username =  email,
        first_name = first_name,
        last_name = last_name,
        email = email,
        mobile = mobile,
        department = teacher.department,
        address = address,
        dob = dob,
        gender = gender,
        created_by = teacher.id
    )
    
    if not account_obj:
        return 100
    
    student_obj = Student.objects.create(
        id = account_obj.id,
        student = account_obj,
        rollno = rollno,
        marks = marks,
        teacher = teacher,
        created_by = teacher.id
    )
    
    if not student_obj:
        return 100
    
    return 201

def updateprofile(first_name,last_name,mobile,dob,gender,address,experience,user):
    obj = Account.objects.get(id=user.id)
    if not obj:
        return 103
    
    obj.first_name = first_name
    obj.last_name = last_name
    obj.mobile = mobile
    obj.dob = dob
    obj.gender = gender
    obj.address = address
    obj.experience = experience
    obj.updated_by = user.id
    obj.save()
    return []

def delete_student(id):
    try:
        student_obj = Account.objects.get(id=id,is_active=True,is_staff=False,is_superuser=False)
        if not student_obj:
            return 103
        student_obj.is_active=False
        student_obj.save()    
        return []
    except Account.DoesNotExist:
      return 103
    
def updatestudent(pk,first_name,last_name,mobile,rollno,dob,gender,address,teacher):
    account_obj = Account.objects.filter(id=pk).last()
    student_obj =  Student.objects.filter(id=pk).last()
    if  not student_obj:
        return 103
    
    if  not account_obj:
        return 103
    
    account_obj.first_name = first_name
    account_obj.last_name = last_name
    account_obj.mobile = mobile
    student_obj.rollno = rollno
    account_obj.dob = dob
    account_obj.gender = gender
    account_obj.address = address
    account_obj.updated_by = teacher.id
    account_obj.save()
    
    return []
    
def get_student_list(user):
    student_queryset = Account.objects.filter(is_active=True,is_staff=False,department=user.department,created_by=user.id)
    if not student_queryset:
        return []
    
    return extract_student_list_to_dict(student_queryset)
    
def get_student_detail(pk,user):
    try:
        student_queryset = Account.objects.get(id=pk,is_active=True,department=user.department)
        if not student_queryset:
            return []
    
        return extract_student_detail_to_dict(student_queryset)
    except:
      return 103   
    
def bulk_student_create(data,teacher):
    emails_ids = [email['email'] for email in data]
    check_email = Account.objects.filter(email__in=emails_ids,is_active=True)
    if check_email:
        return 101
    
    for student in data:
        obj = Account.objects.create(
            username =  student["email"],
            first_name = student["first_name"],
            last_name = student["last_name"],
            email = student["email"],
            mobile = student["mobile"],
            department = teacher.department,
            address = student["address"],
            dob = student["dob"],
            gender = student["gender"],
            created_by = teacher.id
        )
        s_obj = Student.objects.create(
            id = obj.id,
            student = obj,
            rollno = student["rollno"],
            teacher = teacher,
            created_by = teacher.id
        )
    return 201