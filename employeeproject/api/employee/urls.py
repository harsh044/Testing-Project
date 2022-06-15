from django.urls import path
from  . import views as employee_views

urlpatterns = [
    path('register', employee_views.RegisterApiView.as_view(),name="register"),
    path('login', employee_views.LoginApiview.as_view(),name="login"),
    
    path('', employee_views.EmployeeListView.as_view(),name="employee-list"),
    path('retrive/<int:pk>', employee_views.EmployeeRetriveView.as_view(),name="employee-add"),
    path('add', employee_views.EmployeeCreatetView.as_view(),name="employee-add"),
    path('update/<int:pk>', employee_views.EmployeeUpdateView.as_view(),name="employee-update"),
    path('delete/<int:pk>', employee_views.EmployeeDeleteView.as_view(),name="employee-delete"),
]