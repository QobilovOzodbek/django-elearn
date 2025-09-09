# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("course/<int:course_id>/", views.course_detail_view, name="course_detail"),
    path("course/<int:course_id>/lessons/", views.lesson_list_view, name="lesson_list"),
    path("course/<int:course_id>/lesson/<int:lesson_id>/", views.lesson_detail_view, name="lesson_detail"),
    path("course/<int:course_id>/enroll/", views.enroll_course, name="enroll_course"),
    path("profile/", views.profile_view, name="profile"),
    path("certificate/request/<int:course_id>/", views.request_certificate, name="request_certificate"),
    # YANGI:
    path("course/<int:course_id>/lesson/<int:lesson_id>/complete/", views.complete_lesson, name="complete_lesson"),
    path("course/<int:course_id>/module/<int:module_id>/complete/", views.complete_module, name="complete_module"),
]
