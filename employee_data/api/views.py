from django.shortcuts import render
# from flask import Response
# from html5lib import serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import status
# Create your views here.

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def employee_data(request,pk=None):
    if request.method == 'GET':
        id = pk
        if id is not None:
            Emp = Employee.objects.get(id=id)
            serializer = EmployeeSerializer(Emp)
            return Response(serializer.data)
        
        Emp = Employee.objects.all()
        serializer = EmployeeSerializer(Emp,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors)
    
    if request.method == 'PUT':
        id = pk
        Emp = Employee.objects.get(pk=id)
        serializer = EmployeeSerializer(Emp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"Data Updated"},status=status.HTTP_200_OK)
        return Response(serializer.errors)
    
    if request.method == 'PATCH':
        id = pk
        Emp = Employee.objects.get(pk=id)
        serializer = EmployeeSerializer(Emp,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"Partial Data Updated"},status=status.HTTP_200_OK)
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        id = pk
        Emp = Employee.objects.get(pk=id)
        Emp.delete()
        return Response({'Msg':"Data Deleted"},status=status.HTTP_200_OK)