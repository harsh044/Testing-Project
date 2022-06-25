import json
from rest_framework import status, generics
from rest_framework.response import Response
from api.teacher.serializer import CreateRegisterSerializer,CreateLoginSerializer,CreateStudentSerializer,UpdateProfileSerializer,UpdateStudentSerializer
from apps.teacher import service as teacher_service
from common import utils
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class RegisterApiView(generics.GenericAPIView):
    allowed_method = ("POST")
    permission_classes = [IsAuthenticated]
    serializer_class = CreateRegisterSerializer
    
    def post(self,request):
        serializer = CreateRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        user = request.user
        if not user.is_superuser:
            return utils.dispatch_response(107)
        
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        mobile = data['mobile']
        address = data['address']
        experience = data['experience']
        dob = data['dob']
        gender = data['gender']
        password = data['password']
        department = data['department']
        
        validate_response = serializer.validation(data)
        if type(validate_response) == int:
            return utils.dispatch_response(validate_response)
            
        res = teacher_service.register(first_name,last_name,email,mobile,address,experience,dob,gender,password,department,user)
        return utils.dispatch_response(res)

class LoginApiView(generics.GenericAPIView):
    allowed_method = ("POST")
    serializer_class = CreateLoginSerializer
    
    def post(self,request):
        serializer = CreateLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data
        username= data['username']
        password = data['password']
        
        res = teacher_service.login(username,password)
        return utils.dispatch_response(res)

class CreateStudentApiView(generics.GenericAPIView):
    allowed_method = ("POST")
    permission_classes = [IsAuthenticated]
    serializer_class = CreateStudentSerializer
    
    def post(self,request):
        serializer = CreateStudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data
        teacher = request.user
        if not teacher.is_hod:
            return utils.dispatch_response(107)
        
        first_name =  data['first_name']
        last_name =  data['last_name']
        email =  data['email']
        mobile =   data['mobile']
        marks = data['marks']
        dob = data['dob']
        address =   data['address']
        rollno =  data['rollno']
        gender = data['gender']
        
        res = teacher_service.createstudent(first_name,last_name,email,mobile,marks,address,rollno,dob,gender,teacher)
        return utils.dispatch_response(res)
    
class UpdateProfileApiView(APIView):
    allowed_method = ("PUT")
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer
    
    def put(self,request):
        serializer = UpdateProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data
        
        user = request.user
        print(user.is_hod)
        if not user.is_hod and not user.is_superuser:
            return utils.dispatch_response(107)
        
        first_name = data['first_name']
        last_name = data['last_name']
        mobile = data['mobile']
        address = data['address']
        dob = data['dob']
        gender = data['gender']
        experience = data['experience']
    
        res = teacher_service.updateprofile(first_name,last_name,mobile,dob,gender,address,experience,user)
        return utils.dispatch_response(res)
    
class DeleteStudentApiView(APIView):
    allowed_method = ("DELETE")
    permission_classes = [IsAuthenticated]
    
    def delete(self,request,pk):
        user = request.user
        if not user.is_hod:
            return utils.dispatch_response(107)
        
        res = teacher_service.delete_student(pk)
        return utils.dispatch_response(res)
    
class UpdateStudentApiView(APIView):
    allowed_method = ("PUT")
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateStudentSerializer
    
    def put(self,request,pk):
        serializer = UpdateStudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data
        teacher = request.user
        if not teacher.is_hod and not teacher.is_superuser:
            return utils.dispatch_response(107)
        
        first_name = data['first_name']
        last_name = data['last_name']
        mobile = data['mobile']
        address = data['address']
        rollno = data['rollno']
        dob = data['dob']
        gender = data['gender']
    
        res = teacher_service.updatestudent(pk,first_name,last_name,mobile,rollno,dob,gender,address,teacher)
        return utils.dispatch_response(res)
    
class StudentListApiView(APIView):
    allowed_method = ("GET")
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if not user.is_hod:
            return utils.dispatch_response(107)
        
        res = teacher_service.get_student_list(user)
        return utils.dispatch_response(res)
    
class StudentDetailApiView(APIView):
    allowed_method = ("GET")
    permission_classes = [IsAuthenticated]
    
    def get(self,request,pk):
        user = request.user
        if not user.is_hod:
            return utils.dispatch_response(107)
        
        res = teacher_service.get_student_detail(pk,user)
        return utils.dispatch_response(res)
    
class BulkCreateStudentApiView(generics.GenericAPIView):
    allowed_method = ("POST")
    permission_classes = [IsAuthenticated]
    serializer_class = CreateStudentSerializer
    
    def post(self,request):
        serializer = CreateStudentSerializer(data=request.data,many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.initial_data
        teacher = request.user
        if not teacher.is_hod:
            return utils.dispatch_response(107)
        
        res = teacher_service.bulk_student_create(data,teacher)
        return utils.dispatch_response(res)
        
        