from django.contrib import admin

from .forms import StudentForm,AccountForm
from apps.teacher.models import Student,Account
# Register your models here.
admin.site.register(Student, StudentForm)
admin.site.register(Account, AccountForm)