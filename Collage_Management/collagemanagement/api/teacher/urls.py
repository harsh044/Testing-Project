from django.urls import path,include
from . import views as teacher_views

urlpatterns = [
    path('register', teacher_views.RegisterApiView.as_view(),name="register"),
    path('login', teacher_views.LoginApiView.as_view(),name="login"),
    
    path('studentlist', teacher_views.StudentListApiView.as_view(),name="studentlist"),
    path('studentdetail/<int:pk>', teacher_views.StudentDetailApiView.as_view(),name="studentdetail"),
    
    path('createstudent', teacher_views.CreateStudentApiView.as_view(),name="createstudent"),
    path(r'updatestudent/<int:pk>', teacher_views.UpdateStudentApiView.as_view(),name="createstudent"),
    
    path(r'updateprofile', teacher_views.UpdateProfileApiView.as_view(),name="updateprofile"),
    path(r'deletestudent/<int:pk>', teacher_views.DeleteStudentApiView.as_view(),name="deletestudent"),
    
    path(r'bulkcreate', teacher_views.BulkCreateStudentApiView.as_view(),name="bulkcreate"),
]