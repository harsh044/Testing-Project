# from urllib import request
import csv
import re
from tkinter.messagebox import NO
from typing import no_type_check
from urllib import request
from django.contrib import messages
from django.forms import ValidationError
from django import forms
from django.contrib import admin
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from numpy import empty
from apps.teacher.models import Student,Account
from django.utils.html import mark_safe
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group
from django.urls import path
from django.shortcuts import render,redirect
import pandas as pd
from django.db.models import Q
from django.urls import reverse_lazy
from django_admin_listfilter_dropdown.filters import (DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)

class DepartmentListFilter(admin.SimpleListFilter):
    title = 'Department Name'
    parameter_name = 'department'
        
    def lookups(self, request, model_admin):
        department_name = [(1, 'BCOM'),(2,'BSCIT'),(3,'BMM'),(4,'BMS'),(5,'MSCIT'),(6,'MCOM')]
        return department_name
    
    def queryset(self, request, queryset):
        value = self.value()
        if value:
            if request.resolver_match.url_name == 'teacher_account_changelist':
                queryset = queryset.filter(department=value)
            else:
                queryset = queryset.filter(student__department=value)
        return queryset
       
class TeacherNameListFilter(admin.SimpleListFilter):
    title = 'teacher Name'
    parameter_name = 'teacher'
        
    def lookups(self, request, model_admin):
        teacher_name = list(Account.objects.filter(is_active=True,is_hod=True).values_list("id","first_name"))   
        return teacher_name
    
    def queryset(self, request, queryset):
        value = self.value()
        if value:
            queryset = queryset.filter(student__created_by=value)
        return queryset
    
class ColumnListFilter(MultipleChoiceListFilter):
    title = 'Column List display'
    parameter_name = 'list_display'
    template = 'admin/teacher/filter.html'
    
    def lookups(self, request, model_admin):
        column_name = []
        column_name.extend([('name', 'Name'),('rollno', 'Roll No'),('email', 'Email'),('mobile', 'Mobile'),('created_on', 'Created On'),('updated_on', 'Updated on'),('is_active', 'Is_active')])
        
        if request.user.is_superuser:
            column_name.extend([('department', 'Department'),('teacher_name', 'Teacher Name')])
            
        if request.user.is_hod:
            column_name.extend([('created','Created_by')])
            
        return (column_name)
    
    def queryset(self,request,queryset):
        value = self.value()
        pass
    
class IsActiveListFilter(admin.SimpleListFilter):
    title = 'Is Active'
    parameter_name = 'is_active'
        
    def lookups(self, request, model_admin):
        is_active = [(1,"Yes"),(2,"No")]
        return is_active
    
    def queryset(self, request, queryset):
        value = self.value()
        if value:
            try:
                active = True if int(value) == 1 else False
            except:
                return queryset
            if request.resolver_match.url_name == 'teacher_account_changelist':
                queryset = queryset.filter(is_active=active)
            else:
                queryset = queryset.filter(student__is_active=active)
        return queryset
    
class CreateAccountForm(forms.ModelForm):
    DEPARTMENT_CHOICE_TYPE = (
        ("0","--------------"),
        ("1","BCOM"),
        ("2","BSCIT"),
        ("3","BMM"),
        ("4","BMS"),
        ("5","MSCIT"),
        ("6","MCOM")
    )
    GENDER_CHOICE_TYPE = (
        ("0","--------------"),
        ("M","MALE"),
        ("F","FEMALE"),
    )
    
    first_name =  forms.CharField(max_length=50)
    last_name =  forms.CharField(max_length=50)
    email =  forms.CharField(max_length=50)
    rollno =  forms.CharField(max_length=10)
    phone_regex = RegexValidator(regex=r'[0-9]{10,15}', message="Invalid phone number")
    mobile =  forms.CharField(max_length=50,validators=[phone_regex])
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'cols':20,'style':'max-width:100%;min-width:100%;min-height:130px;max-height:100px;'}),required=False)
    dob =  forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICE_TYPE, required=True)
    experience =  forms.IntegerField()
    department =  forms.ChoiceField(choices=DEPARTMENT_CHOICE_TYPE, required=True)
    
    class Meta:
        model = Account
        fields = ["first_name","last_name","email","rollno","mobile","address","dob","gender","experience","department"]
        
    def clean(self):
        cleaned_data = super(CreateAccountForm, self).clean()
        # print(cleaned_data)
        if self.initial == 0:
            email = cleaned_data.get("email")
            mobile = cleaned_data.get("mobile")
            gender = cleaned_data.get("gender")
            department = cleaned_data.get("department")
            email = Account.objects.filter(email=email)
            mobile = Account.objects.filter(mobile=mobile)
            if email:
                raise ValidationError({"email":"Email Id is Already Exists"})
            
            if mobile:
                raise ValidationError({"mobile":"Mobile No Already Exists"}) 
            
            if gender == "0":
                raise ValidationError({'gender':"Please Select Gender"})
            
            if department == "0":
                raise ValidationError({'department':"Please Select Department"})
        
class CreateStudentForm(forms.ModelForm):
    DEPARTMENT_CHOICE_TYPE = (
        ("0","--------------"),
        ("1","BCOM"),
        ("2","BSCIT"),
        ("3","BMM"),
        ("4","BMS"),
        ("5","MSCIT"),
        ("6","MCOM")
    )
    GENDER_CHOICE_TYPE = (
        ("0","--------------"),
        ("M","MALE"),
        ("F","FEMALE"),
    )
    
    first_name =  forms.CharField(max_length=50)
    last_name =  forms.CharField(max_length=50)
    email =  forms.CharField(max_length=50)
    rollno =  forms.CharField(max_length=10)
    phone_regex = RegexValidator(regex=r'[0-9]{10,15}', message="Invalid phone number")
    mobile =  forms.CharField(max_length=50,validators=[phone_regex])
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'cols':20,'style':'max-width:100%;min-width:100%;min-height:130px;max-height:100px;'}),required=False)
    dob =  forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICE_TYPE)
    department =  forms.ChoiceField(choices=DEPARTMENT_CHOICE_TYPE)
    
    class Meta:
        model = Account
        fields = ["first_name","last_name","email","rollno","mobile","address","dob","gender","department"]
        
    def clean(self):
        cleaned_data = super(CreateStudentForm, self).clean()
        # print(cleaned_data)
        if not bool(self.initial):
            email = cleaned_data.get("email")
            mobile = cleaned_data.get("mobile")
            gender = cleaned_data.get("gender")
            department = cleaned_data.get("department")
            email_exists = Account.objects.filter(email=email)
            mobile_exists = Account.objects.filter(mobile=mobile)
            
            if len(email) > 0 and email_exists.count()>0:
                raise ValidationError({"email":"Email Id is Already Exists"})
            
            if len(mobile) > 0 and mobile_exists.count()>0:
                raise ValidationError({"mobile":"Mobile No Already Exists"}) 
            
            if gender == '0':
                raise ValidationError({'gender':"Please Select Gender"})
        
            if department == '0':
                raise ValidationError({'department':"Please Select Department"})
                          
class StudentForm(admin.ModelAdmin):    
    form = CreateStudentForm
    actions = ['export_student','delete_student']
    super_obj = Account.objects.filter(is_superuser=True).last()
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload_csv/',self.upload_csv,name="upload-student"),]
        return new_urls + urls
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    @staticmethod
    def validate_email_mobile(df):
        email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        mobile_pattern = re.compile(r"[0-9]{10,15}")
        
        new_df=pd.DataFrame()
        new_df['isemail']=df['EMAIL'].apply(lambda x: True if email_pattern.match(x) else False)
        new_df['ismobile']=df['MOBILE'].apply(lambda x: True if mobile_pattern.match(x) else False)
        is_email = False if new_df[new_df["isemail"] == False].shape[0] > 0 else True
        is_mobile = False if new_df[new_df["ismobile"] == False].shape[0] > 0 else True
        return is_email,is_mobile
    
    def upload_csv(self,request):
        if request.method == "POST":
            file = request.FILES["csv_upload"]
            file_name = file.name
            file_extension = file_name.split('.')[-1]
            
            if file_extension.upper() not in ['CSV','EXCEL']:
                messages.error(request, "Invalid file type")
                return redirect(request.path_info)
            
            if file_extension.upper() == "CSV":
                df = pd.read_csv(file,dtype={'mobile':str,'gender':str,'email':str,'First Name':str,'Last Name':str,'Roll No':int})
            else:
                df = pd.read_csv(file,sheet_name=0,engine='openpyxl',dtype={'mobile':str,'gender':str,'email':str,'First Name':str,'Last Name':str,'Roll No':int},errors="coerce")
            
            headers = ["FIRST NAME","LAST NAME","EMAIL","MOBILE","ADDRESS","GENDER","DOB","ROLL NO"]
            df.columns = df.columns.str.upper()
            df_headers = df.columns.tolist()
            if len(df_headers) == 0:
                messages.error(request, "invalid headers")
                return redirect(request.path_info)
            
            diff_header = list(set(df_headers).difference(headers))
            if len(diff_header) > 0:
                messages.error(request, "Headers don't match")
                return redirect(request.path_info)
            
            df = df.dropna(how='all')
            if df.empty:
                messages.error(request, "The uploaded files has no student data")
                return redirect(request.path_info)
            
            user = request.user

            df["DOB"] = pd.to_datetime(df["DOB"],errors="coerce")
                
            if df['FIRST NAME'].isnull().any():
                messages.error(request, "First Name Column Contain Null Value")
                return redirect(request.path_info)
            
            if df['LAST NAME'].isnull().any():
                messages.error(request, "Last Name Column Contain Null Value")
                return redirect(request.path_info)
            
            if df['EMAIL'].isnull().any():
                messages.error(request, "Email ID Column Contain Null Value")
                return redirect(request.path_info)
            
            if df['MOBILE'].isnull().any():
                messages.error(request, "Mobile Column Contain Null Value")
                return redirect(request.path_info)
            
            if df['GENDER'].isnull().any():
                messages.error(request, "Gender Column Contain Null Value")
                return redirect(request.path_info)
            
            if df["DOB"].isna().any() or df['DOB'].isnull().any():
                messages.error(request, "DOB column contains invalid date")
                return redirect(request.path_info)
            
            if df['ROLL NO'].isnull().any():
                messages.error(request, "Roll No Column Contain Null Value")
                return redirect(request.path_info)
            
            is_email,is_mobile = self.validate_email_mobile(df)
            if not is_email:
                messages.error(request, "Email column contains invalid email id")
                return redirect(request.path_info)
            
            if not is_mobile:
                messages.error(request, "mobile column contains invalid mobile number")
                return redirect(request.path_info)
            
            g = df[~df["GENDER"].isin(['M','F'])]
            if g.shape[0]>0:
                messages.error(request, "Gender column contains invalid gender type")
                return redirect(request.path_info)
            
            email_ids = df['EMAIL'].tolist()
            check_email = Account.objects.filter(email__in=email_ids,is_active=True)
            super_obj = Account.objects.filter(is_superuser=True).last()
            if user.is_hod:
                check_email = check_email.filter(Q(created_by=user.id) | Q(created_by=super_obj.id))
            stud_email_ids = list(check_email.values_list('email',flat=True))
            df = df[~df["EMAIL"].isin(stud_email_ids)]
            count = 0
            for index,data in df.iterrows():
                first_name=data['FIRST NAME']
                last_name=data['LAST NAME']
                email=data['EMAIL']
                mobile=data['MOBILE']
                address=data['ADDRESS']
                gender=data['GENDER']
                dob=data['DOB']
                rollno=data['ROLL NO']
                                
                obj=Account.objects.create(first_name=first_name,
                                           last_name=last_name,
                                           email=email,
                                           mobile=mobile,
                                           address=address,
                                           gender=gender,
                                           dob=dob,
                                           department=user.department,
                                           username=email,
                                           created_by=user.id
                                           )
                
                student_obj = Student.objects.create(id=obj.id,
                                                     student=obj,
                                                     rollno=rollno,
                                                     teacher=user,
                                                     created_by=user.id)
                if obj and student_obj:
                    count += 1
                    
            if count > 0:
                msg = "{} student created successfully".format(count)
                messages.success(request, msg)
                
            if len(stud_email_ids) > 0 and count > 0:
                msg += "and {} student already exists".format(len(stud_email_ids))
                messages.warning(request, msg)
            else:
                msg = "{} student already exists".format(len(stud_email_ids))
                messages.error(request, msg)
            
            return HttpResponseRedirect(reverse_lazy('admin:teacher_student_changelist'))      
            
        return render(request,"admin/teacher/student/csv_create.html")
    
    def export_student(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)
        if request.user.is_superuser:
            writer.writerow(['First Name','Last Name','email','mobile','address','gender','DOB','Roll No','Department','Teacher Name','is_active'])
            for student  in queryset.values_list('student__first_name','student__last_name','student__email','student__mobile','student__address','student__gender','student__dob','rollno','student__department','teacher__first_name','student__is_active'):
                writer.writerow(student)
        else:
            writer.writerow(['First Name','Last Name','email','mobile','address','gender','DOB','Roll No','is_active'])
            for student  in queryset.values_list('student__first_name','student__last_name','student__email','student__mobile','student__address','student__gender','student__dob','rollno','student__is_active'):
                writer.writerow(student)
        
        return response
        
    export_student.short_description = 'Export Student'
    
    def delete_student(self, request, queryset):
        user = request.user
        student_ids = list(queryset.values_list('id',flat=True))
        self_created = list(queryset.filter(created_by=user.id,id__in=student_ids).values_list('id',flat=True))
        not_created = list(set(student_ids) - set(self_created))
        Account.objects.filter(id__in=self_created).delete()
        if len(self_created) > 0 and len(not_created) > 0:
            msg = "{} student deleted successfully and {} student not created by you".format(len(self_created),len(not_created))
            messages.warning(request,msg)
                
        elif len(not_created) > 0 and not len(self_created) > 0:
            msg = "{} student not created by you".format(len(not_created))
            messages.error(request,msg)
            
        elif not len(not_created) > 0 and len(self_created) > 0:
            msg = "{} student deleted successfully".format(len(self_created))
            messages.success(request,msg)
    
    def get_list_display(self, request):
        field = ['name','rollno','email','mobile','created_on','updated_on','is_active']
        filter_list = request.GET.get('list_display')
        if filter_list:
            filter_list = filter_list.split(',')
            field = filter_list
        else:
            if request.user.is_hod:
                field.append("created")
        
        if request.user.is_superuser:
            if not filter_list:
                field.extend(['department','teacher_name'])
            return field
        return field

    def get_list_filter(self, request):
        permission_with_super = (DepartmentListFilter,TeacherNameListFilter,IsActiveListFilter,ColumnListFilter)
        
        if request.user.is_superuser:
            return permission_with_super
        return [IsActiveListFilter,ColumnListFilter]  
    
    def is_active(self,obj):
        if obj.student.is_active:
            return mark_safe('<img src="/static/admin/img/icon-yes.svg">')
        return mark_safe('<img src="/static/admin/img/icon-no.svg">')
            
    def get_search_fields(self, request):
        if request.user.is_superuser:
            return ('student__department','student__first_name','teacher__first_name')
        return ("student__first_name",)
        
    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
                request, queryset, search_term,
            )
        if search_term:
            department_id = 1 if search_term.upper() in "BCOM" else 2 if search_term.upper() in "BSCIT" else 3 if search_term.upper() in "BMM" else 4 if search_term.upper() in "BMS" else 5 if search_term.upper() in "MSCIT" else 6 if search_term.upper() in "MCOM" else 0
            if department_id == 0:
                return queryset, may_have_duplicates
            queryset |= Student.objects.filter(student__department=department_id)
        return queryset,may_have_duplicates
    
    def name(self,obj):
        if obj is None:
            return "-"
        return obj.student.first_name +' '+ obj.student.last_name
    
    def email(self,obj):
        if obj is None:
            return "-"
        return obj.student.email
    
    def department(self,obj):
        if obj.student is None:
            return "-"
        
        if obj.student.department == 6:
            return "MCOM"
        elif obj.student.department == 5:
            return "MSCIT"
        elif obj.student.department == 4:
            return "BMS"
        elif obj.student.department == 3:
            return "BMM"
        elif obj.student.department == 2:
            return "BSCIT"
        elif obj.student.department == 1:
            return "BCOM"
        else:
            return "-"

    def mobile(self,obj):
        if obj.student is None:
            return "-"
        
        return obj.student.mobile

    def teacher_name(self,obj):
        if obj.student is None:
            return "-"
        if self.super_obj.id == obj.created_by:
            return "Super Admin"
        return obj.teacher.first_name
    
    def created(self,obj):
        if obj.created_by == self.super_obj.id:
            return "super admin"
        return "self"
    created.short_description = "created_by"
    
    @transaction.atomic
    def save_model(self, request, obj, form, change):
        try:
            # print(form.cleaned_data)
            id = obj.id
            user = request.user
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            mobile = form.cleaned_data['mobile']
            department = form.cleaned_data['department'] if user.is_superuser else user.department
            address = form.cleaned_data['address']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']
            rollno = form.cleaned_data['rollno']
                            
            account_obj,created = Account.objects.update_or_create(
                id = id,
                defaults= {
                    'first_name' : first_name,
                    'last_name' : last_name,
                    'email' : email,
                    'username' : email,
                    'mobile' : mobile,
                    'department' : department,
                    'address' : address,
                    'dob' : dob,
                    'gender' : gender,
                    'created_by' : user.id
                }
                
            )
            obj.id = account_obj.id
            obj.created_by = request.user.id
            obj.teacher = user
            obj.student = account_obj
            obj.rollno = rollno
            obj.save()
        except Exception as err:
            print(err)
            transaction.set_rollback(True)
            
    def get_form(self, request, obj=None, **kwargs):
        form = super(StudentForm, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            del form.base_fields['department']
        form.base_fields['first_name'].initial = ""
        form.base_fields['last_name'].initial = ""
        form.base_fields['email'].initial = ""
        form.base_fields['rollno'].initial = ""
        form.base_fields['mobile'].initial = ""
        form.base_fields['address'].initial = ""
        form.base_fields['dob'].initial = ""
        form.base_fields['gender'].initial = ""
        if request.user.is_superuser:
            form.base_fields['department'].initial = ""
        
        if obj:
            form.base_fields['first_name'].initial = obj.student.first_name
            form.base_fields['last_name'].initial = obj.student.last_name
            form.base_fields['email'].initial = obj.student.email
            form.base_fields['mobile'].initial = obj.student.mobile
            form.base_fields['address'].initial = obj.student.address
            form.base_fields['dob'].initial = obj.student.dob
            form.base_fields['gender'].initial = obj.student.gender
            
            if obj.created_by != request.user.id:
                form.base_fields['first_name'].widget.attrs['disabled'] = True
                form.base_fields['last_name'].widget.attrs['disabled'] = True
                form.base_fields['email'].widget.attrs['disabled'] = True
                form.base_fields['mobile'].widget.attrs['disabled'] = True
                form.base_fields['address'].widget.attrs['disabled'] = True
                form.base_fields['dob'].widget.attrs['disabled'] = True
                form.base_fields['gender'].widget.attrs['disabled'] = True
                form.base_fields['rollno'].widget.attrs['disabled'] = True
            else:
                form.base_fields['first_name'].widget.attrs['disabled'] = False
                form.base_fields['last_name'].widget.attrs['disabled'] = False
                form.base_fields['email'].widget.attrs['disabled'] = False
                form.base_fields['mobile'].widget.attrs['disabled'] = False
                form.base_fields['address'].widget.attrs['disabled'] = False
                form.base_fields['dob'].widget.attrs['disabled'] = False
                form.base_fields['gender'].widget.attrs['disabled'] = False
                form.base_fields['rollno'].widget.attrs['disabled'] = False
                
            
            if request.user.is_superuser:
                form.base_fields['department'].initial = obj.student.department
                if obj.created_by != request.user.id:
                    form.base_fields['department'].widget.attrs['disabled'] = True
                else:
                    form.base_fields['department'].widget.attrs['disabled'] = False
                                         
        return form

    def render_change_form(self, request, context, add, change, form_url, obj):
        change_form = super().render_change_form(request, context, add, change, form_url, obj)
        if obj and obj.created_by != request.user.id:
            context.update({
                "has_change_permission" : False,
                "has_view_permission" : True,
                "has_delete_permission" : False
            })

        return change_form

    def get_queryset(self, request):
        user = request.user.id
        queryset = Student.objects.filter(student__is_active=True)
        if request.user.is_hod:
            queryset = queryset.filter(Q(student__created_by=user) | Q(student__created_by=self.super_obj.id))
        return queryset
              
class AccountForm(admin.ModelAdmin):
    form = CreateAccountForm
    list_display=("name",'email','mobile','is_active','created_on','updated_on','department_name','total_student')
    search_fields = ['department','first_name','email']
    
    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term,
        )
        department_id = 1 if search_term.upper() in "BCOM" else 2 if search_term.upper() in "BSCIT" else 3 if search_term.upper() in "BMM" else 4 if search_term.upper() in "BMS" else 5 if search_term.upper() in "MSCIT" else 6 if search_term.upper() in "MCOM" else 0
        if department_id == 0:
            return queryset, may_have_duplicates
        queryset |= Account.objects.filter(is_hod=True,department=department_id)
        return queryset,may_have_duplicates
    
    def name(self,obj):
        return obj.first_name +' '+ obj.last_name
    
    def department_name(self,obj):
        if obj.department is None:
            return "-"
        if obj.department == 6:
            return "MCOM"
        elif obj.department == 5:
            return "MSCIT"
        elif obj.department == 4:
            return "BMS"
        elif obj.department == 3:
            return "BMM"
        elif obj.department == 2:
            return "BSCIT"
        elif obj.department == 1:
            return "BCOM"
        else:
            return "-"
        
    def total_student(self,obj):
        student_count = Account.objects.filter(created_by=obj.id).count()
        return student_count
    
    @transaction.atomic
    def save_model(self, request, obj, form, change):
        try:
            group = Group.objects.filter(name="admin").last()
            email = form.cleaned_data['email']
            obj.is_hod = True
            obj.is_staff = True
            obj.created_by = request.user.id
            obj.username = email
            obj.save()
            obj.groups.add(group)
            obj.save()
        except Exception as err:
            print(err)
            transaction.set_rollback(True)
            
    def get_form(self, request, obj=None, **kwargs):
        form = super(AccountForm, self).get_form(request, obj, **kwargs)
        del form.base_fields['rollno']
        form.base_fields['first_name'].initial = ""
        form.base_fields['last_name'].initial = ""
        form.base_fields['email'].initial = ""
        form.base_fields['mobile'].initial = ""
        form.base_fields['address'].initial = ""
        form.base_fields['dob'].initial = ""
        form.base_fields['gender'].initial = ""
        form.base_fields['experience'].initial = ""
        form.base_fields['department'].initial = ""

        if obj:
            form.base_fields['first_name'].initial = obj.first_name
            form.base_fields['last_name'].initial = obj.last_name
            form.base_fields['email'].initial = obj.email
            form.base_fields['mobile'].initial = obj.mobile
            form.base_fields['address'].initial = obj.address
            form.base_fields['dob'].initial = obj.dob
            form.base_fields['gender'].initial = obj.gender
            form.base_fields['experience'].initial = obj.experience
            form.base_fields['department'].initial = obj.department

        return form
        
    def get_queryset(self, request):
        queryset = Account.objects.filter(is_hod=True)
        return queryset
    
    def get_list_filter(self, request):
        permission_with_super = (DepartmentListFilter,IsActiveListFilter)
        return permission_with_super
    
    def delete_model(self, request, obj):
        delete = Account.objects.filter(id=obj.id).delete()
        return delete
    
    
        
                
        