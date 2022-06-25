from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.
class Employee(models.Model):
    name=models.CharField(max_length=100)
    designation=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    salary=models.IntegerField(max_length=50)