from pyexpat.errors import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from django.contrib import messages

# Create your views here.
def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active and user.is_superuser:
                login(request,user)
                return redirect('admin_custm:home')
            messages.error(request,"You Are Not Authorized User")
        else:
            messages.error(request,"Username Or Password not correct")
    else:
        form = AuthenticationForm()
    return render(request,"admin/auth/login.html",{'form':form})

@login_required(login_url="/employee-admin/login/")
def home(request):
    return HttpResponse("Welcome")