from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from common.utils import generate_password

# Create your models here.
class Account(AbstractUser):
    class Meta:
        db_table = "auth_user"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
    
    mobile = models.CharField(max_length=15,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    department = models.IntegerField(null=True,blank=True)
    is_hod = models.BooleanField(default=False,null=True,blank=True)
    experience = models.CharField(max_length=50,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=2,null=True,blank=True)
    created_by = models.IntegerField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.password is None or self.password is '':
            password = generate_password(self.email)
            self.set_password(password)
            print("password",password)
        self.full_clean()
        super().save(*args, **kwargs)

class Student(models.Model):
    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'
        
    id = models.PositiveIntegerField(primary_key=True,verbose_name='ID')
    student = models.ForeignKey(Account, on_delete=models.CASCADE,null=True,related_name="map_with_student")
    teacher = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    rollno = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True,blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.student)