from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib import admin

from apps.teacher.models import Account, Student

# Create your views here.
def landing(request):
    return render(request, 'admin/landing_page/landing.html', context={})

def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active and (user.is_superuser or user.is_hod):
                login(request,user)
                return redirect('admin:index')
            messages.error(request,"You are not authorized user")
        else:
            messages.error(request,"username or password not correct")
    else:
        form = AuthenticationForm()
    return render(request,'admin/auth/login.html',{'form': form})

class AdminSiteLayout(admin.AdminSite):
    pass

admin_site = AdminSiteLayout()
def get_login_context(request):
    context = {
        'user': request.user,
        'site_header': admin_site.site_header,
        'has_permission': admin_site.has_permission(request),
        'site_url': admin_site.site_url
    }
    return context

@login_required(login_url="/college-admin/login/")
def home(request):
    context = get_login_context(request)
    counts = {
        "account": get_accounts_count(context),
        "student": get_student_count(context),
    }
    context.update(counts)
    return render(request,'admin/home/index.html',context=context)
    
def get_accounts_count(context):
    counts = Account.objects.filter(is_hod=True,is_active=True)
    counts = counts.count()
    return counts
        
def get_student_count(context):
    user = context.get("user")
    counts = Student.objects.filter(student__is_active=True)
    if user.is_hod:
        counts = counts.filter(created_by=user.id)

    counts = counts.count()
    return counts

def logout(request):
    logout(request)
    response = redirect('/home')
    response.delete_cookie('example_cookie')
    return response

@login_required(login_url="/college-admin/login/")
def change_password(request):
    context = get_login_context(request)
    if request.method == "POST":
        old_pass = request.POST['old_pass']
        new_pass = request.POST['new_pass']
        conf_pass = request.POST['conf_pass']
        
        check_old_pass =  Account.objects.filter(id=request.user.id).last()
        if not check_old_pass.check_password(old_pass):
            messages.error(request,"Password Not Match")
        
        elif new_pass != conf_pass:
            messages.error(request,"New Password and Confirm Password Not Match")
            
        elif check_old_pass.check_password(new_pass):
            messages.error(request,"New password Not Same as Old Password")
            
        else:
            check_old_pass.set_password(new_pass)
            check_old_pass.save()
            return redirect('college-admin')
        
    return render(request, 'registration/password_change_form.html',context=context)
    
    