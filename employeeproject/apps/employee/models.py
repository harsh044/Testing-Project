from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Employee(AbstractUser):
    class Meta:
        db_table = "auth_user"
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        
    designation = models.CharField(max_length=50,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    salary = models.FloatField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email