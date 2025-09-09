from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course
from .models import CertificateRequest

@login_required
def request_certificate(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Avval ariza mavjudmi, tekshiramiz
    existing = CertificateRequest.objects.filter(student=request.user, course=course).first()
    if existing:
        messages.warning(request, "Siz bu kurs uchun allaqachon ariza yuborgansiz.")
    else:
        CertificateRequest.objects.create(student=request.user, course=course, status="pending")
        messages.success(request, "Sertifikat olish uchun ariza yuborildi!")

    return redirect("profile")
