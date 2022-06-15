# from ctypes import util
# from tkinter.messagebox import NO
# from urllib import request
# from apps import employee
# from apps.employee.models import Employee
from tkinter import N
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.employee.serializer import CreateEmployeeSerializer,CreateRegisterSerializer,CreateLoginSerializer
from rest_framework import status, generics
from apps.employee import service as employee_service
from apps.employee import validators as employee_validate
from common import utils
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Authentication Functions
class RegisterApiView(generics.GenericAPIView):
    allowed_method = ("POST")
    serializer_class = CreateRegisterSerializer
    
    def post(self,request):
        serializer = CreateRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        username= data['username']
        password = data['password']
        # print(password)
        
        validate_response = employee_validate.validate_password(password)
        if type(validate_response) == int:
            return utils.dispatch_response(validate_response)
            
        res = employee_service.register(first_name,last_name,email,username,password)
        return utils.dispatch_response(res)

class LoginApiview(generics.GenericAPIView):
    allowed_method = ("POST")
    serializer_class = CreateLoginSerializer
    
    def post(self,request):
        serializer = CreateLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data
        username= data['username']
        password = data['password']
        
        res = employee_service.login(username,password)
        return utils.dispatch_response(res)

# CRUD Functions
class EmployeeListView(APIView):
    permissions_class = [IsAuthenticated]
    allowed_method = ("GET")
    def get(self, request):
        res = employee_service.get_employee_list()
        return utils.dispatch_response(res)
    
class EmployeeRetriveView(APIView):
    permissions = [IsAuthenticated]
    allowed_method = ("GET")
    def get(self, request, pk):
        res = employee_service.get_employee_details(pk)
        return utils.dispatch_response(res)

class EmployeeCreatetView(generics.GenericAPIView):
    permissions = [IsAuthenticated]
    allowed_method = ("POST")
    serializer_class = CreateEmployeeSerializer

    def post(self,request):
        serializer = CreateEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data
        salary = None
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        city = data['city']
        designation = data['designation']
        
        if "salary" in data.keys():
            salary = data['salary']
            
        validate_response = employee_validate.validate_employee_details(salary)
        if type(validate_response) == int:
            return utils.dispatch_response(validate_response)
            
        res = employee_service.create_employee(first_name,last_name,email,city,designation,salary)
        return utils.dispatch_response(res)

class EmployeeUpdateView(APIView):
    permissions = [IsAuthenticated]
    allowed_method = ("PUT")
    serializer_class = CreateEmployeeSerializer
    def put(self,request,pk):
        serializer = CreateEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data
        salary = None
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        city = data['city']
        designation = data['designation']
        
        if "salary" in data.keys():
            salary = data['salary']
            
        validate_response = employee_validate.validate_employee_details(salary)
        if type(validate_response) == int:
            return utils.dispatch_response(validate_response)
        
        res = employee_service.update_employee(pk,first_name,last_name,email,city,designation,salary)
        return utils.dispatch_response(res)

class EmployeeDeleteView(APIView):
    permissions = [IsAuthenticated]
    allowed_method = ("DELETE")
    def delete(self,request,pk):
        res = employee_service.delete_employee(pk)
        return utils.dispatch_response(res)