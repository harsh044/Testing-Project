from django.urls import path
from . import views as admin_views

urlpatterns = [
    path('',admin_views.home,name="home")
]
