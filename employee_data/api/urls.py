from django import views
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path(r'api/', views.employee_data),
    path(r'api/<int:pk>/', views.employee_data),
]