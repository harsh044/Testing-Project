from django.contrib import admin
from matplotlib.pyplot import cla
from .models import Employee
# Register your models here.
@admin.register(Employee)
class Employee(admin.ModelAdmin):
    list_display = ['id','name','designation','city','salary']