from django.urls import path
from . import views as admin_views

urlpatterns = [
    path('',admin_views.home,name="home"),
    path('change_password',admin_views.change_password,name="change_password"),
]