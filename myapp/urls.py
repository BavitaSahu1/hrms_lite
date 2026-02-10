from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('base_admin',views.base_admin,name="base_admin"),
    path('base_dashboard',views.base_dashboard,name="base_dashboard"),
    path('',views.dashboard,name="dashboard"),
    path('Registration',views.add_emp,name="add_emp"),
    path('saveEmployeeData',views.saveEmployeeData,name="saveEmployeeData"),
    path('employees',views.view_emp,name="view_emp"),
    path('DeleteEmp',views.DeleteEmp,name="DeleteEmp"),
    path('Attendance',views.view_attendance,name="view_attendance"),
    path('MarkAttendance',views.MarkAttendance,name="MarkAttendance"),  
    # path('UpdateAttendance',views.UpdateAttendance,name="UpdateAttendance"),  
    # path('EditAttStatus',views.EditAttStatus,name="EditAttStatus"),
]
