from django.urls import path
from . import views

urlpatterns = [
    path("request/<int:course_id>/", views.request_certificate, name="request_certificate"),
]
