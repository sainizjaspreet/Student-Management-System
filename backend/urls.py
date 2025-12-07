from django.contrib import admin
from django.urls import path
from students import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("students/", views.student_list, name="student_list"),
    path("students/add/", views.student_create, name="student_create"),
    path("attendance/", views.attendance_list, name="attendance_list"),
    path("attendance/mark/", views.attendance_mark, name="attendance_mark"),
    path("marks/", views.marks_list, name="marks_list"),
    path("marks/add/", views.marks_add, name="marks_add"),
]
