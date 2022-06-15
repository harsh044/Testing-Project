# from apps import employee
import jwt
from apps.employee.models import Employee
from apps.employee.model_parser import extract_employee_list_to_dict,extract_employee_details_to_dict
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from api.employee.serializer import UserDetailSerializeer

# Register Function
def register(first_name,last_name,email,username,password):
    check_if_email_exists = Employee.objects.filter(email=email)
    if check_if_email_exists:
        return 101
    
    user_obj = Employee.objects.create(
        first_name = first_name,
        last_name = last_name,
        email = email,
        username = username,
        password = password
    )
    if not user_obj:
        return 100
    
    user_obj.set_password(password)
    user_obj.save()
    
    return 201


def get_token_from_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Login Function
def login(username,password):
    user_obj = Employee.objects.filter(username=username,is_active=True).last()
    
    if not user_obj:
        return 105
    
    if not user_obj.check_password(password):
        return 106
    
    jwt_response = get_token_from_user(user_obj)
    if not jwt_response:
        return 100
    
    
    bearer_token = {key: f"{settings.AUTH_PREFIX} {val}" for key, val in jwt_response.items()}
    user_details = UserDetailSerializeer(user_obj)
    return {
        "token" : bearer_token,
        "user_details" : user_details.data
    }
    
# Create Employee Data Function
def create_employee(first_name,last_name,email,city,designation,salary):
    check_if_email_exists = Employee.objects.filter(email=email)
    if check_if_email_exists:
        return 101
    
    employee_obj = Employee.objects.create(
        first_name = first_name,
        last_name = last_name,
        email = email,
        city = city,
        designation = designation,
        salary = salary,
        username = email
    )
    
    if not employee_obj:
        return 100
    
    return 201

# Get Employee List Data Function
def get_employee_list():
    emp_queryset = Employee.objects.filter(is_active=True).exclude(is_superuser=True)
    if not emp_queryset:
        return []
    
    return extract_employee_list_to_dict(emp_queryset)

# Get Employee Details Data Function
def get_employee_details(employee_id):
    emp_obj = Employee.objects.filter(id=employee_id).last()
    if not emp_obj:
        return []
    
    return extract_employee_details_to_dict(emp_obj)

# Delete Employee Data Function
def delete_employee(employee_id):
    emp_obj =  Employee.objects.filter(id=employee_id).last()
    if not emp_obj:
        return 103
    
    emp_obj.delete()
    return []

# Update Employee Data Function
def update_employee(pk,first_name,last_name,email,city,designation,salary):
    emp_obj = Employee.objects.filter(id=pk).last()
    if  not emp_obj:
        return 103
    
    emp_obj.first_name = first_name
    emp_obj.last_name = last_name
    emp_obj.email = email
    emp_obj.city = city
    emp_obj.designation = designation
    emp_obj.salary = salary
    emp_obj.save()
    
    return []