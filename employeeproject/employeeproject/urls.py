from django.contrib import admin
from django.urls import path,re_path
from django.urls import path,include
from apps.admin_custom import views as admin_custom_view

urlpatterns = [
    re_path(r'^employee-admin/login/$', admin_custom_view.loginView,name="admin_login"),
    re_path(r'^employee-admin/', include(("apps.admin_custom.urls","admin_custm"),namespace="admin_custom")),
    path('admin/', admin.site.urls),
    path('employee/', include("api.employee.urls")),
]
