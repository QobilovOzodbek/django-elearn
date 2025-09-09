# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Module, Lesson, Enrollment, LessonCompletion, ModuleCompletion
from certificates.models import CertificateRequest, Certificate
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

def _course_progress(user, course):
    total = Lesson.objects.filter(module__course=course).count()
    done = LessonCompletion.objects.filter(student=user, lesson__module__course=course).count()
    return int(done * 100 / total) if total else 0

def home_view(request):
    course_list = Course.objects.all().order_by("-id")
    paginator = Paginator(course_list, 6)  # har sahifada 6 ta kurs
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {"page_obj": page_obj})

def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.filter(course=course).order_by("order").prefetch_related("lessons")

    is_enrolled = False
    progress = 0
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        if is_enrolled:
            progress = _course_progress(request.user, course)

    return render(request, "course_detail.html", {
        "course": course,
        "modules": modules,
        "is_enrolled": is_enrolled,
        "progress": progress,
    })

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request, f"Siz '{course.title}' kursiga muvaffaqiyatli yozildingiz!")
    else:
        messages.info(request, f"Siz allaqachon '{course.title}' kursiga yozilgansiz.")
    return redirect("course_detail", course_id=course.id)

def lesson_list_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = request.user.is_authenticated and Enrollment.objects.filter(student=request.user, course=course).exists()
    if not is_enrolled:
        return redirect("course_detail", course_id=course.id)
    modules = Module.objects.filter(course=course).order_by("order").prefetch_related("lessons")
    return render(request, "lesson_list.html", {"course": course, "modules": modules})

@login_required
def lesson_detail_view(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    if not is_enrolled:
        messages.warning(request, "Avval kursga yoziling!")
        return redirect("course_detail", course_id=course.id)

    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    # Navigatsiya: shu modul ichidagi oldingi/next dars
    prev_lesson = Lesson.objects.filter(module=lesson.module, order__lt=lesson.order)\
                                .order_by("-order").first()
    next_lesson = Lesson.objects.filter(module=lesson.module, order__gt=lesson.order)\
                                .order_by("order").first()

    # Keyingi modulning birinchi darsi
    next_module = Module.objects.filter(course=course, order__gt=lesson.module.order)\
                                .order_by("order").prefetch_related("lessons").first()
    next_module_first = next_module.lessons.first() if next_module else None

    # Dars tugallanganmi?
    is_completed = LessonCompletion.objects.filter(student=request.user, lesson=lesson).exists()

    progress = _course_progress(request.user, course)

    return render(request, "lesson_detail.html", {
        "course": course,
        "lesson": lesson,
        "prev_lesson": prev_lesson,
        "next_lesson": next_lesson,               # mavjud bo‘lsa — Keyingi
        "next_module_first": next_module_first,   # yo‘q bo‘lsa — Modulni yakunlash -> keyingi modulga
        "is_completed": is_completed,
        "progress": progress,
    })

@login_required
def complete_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    if not is_enrolled:
        return redirect("course_detail", course_id=course.id)

    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    LessonCompletion.objects.get_or_create(student=request.user, lesson=lesson)

    # Agar shu modulda keyingi dars bo‘lsa — o‘sha darsga o‘tamiz
    next_lesson = Lesson.objects.filter(module=lesson.module, order__gt=lesson.order)\
                                .order_by("order").first()
    if next_lesson:
        messages.success(request, "Dars tugallandi. Keyingi darsga o‘tildi.")
        return redirect("lesson_detail", course_id=course.id, lesson_id=next_lesson.id)

    # Aks holda shu dars sahifasiga qaytamiz va "Modulni yakunlash" tugmasi ko‘rinadi
    messages.info(request, "Dars tugallandi. Endi modulni yakunlashingiz mumkin.")
    return redirect("lesson_detail", course_id=course.id, lesson_id=lesson.id)

@login_required
def complete_module(request, course_id, module_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)

    # Shu moduldagi barcha darslarni tugallangan deb belgilab qo‘yamiz (agar belgilanmagan bo‘lsa)
    lessons = module.lessons.all()
    for l in lessons:
        LessonCompletion.objects.get_or_create(student=request.user, lesson=l)

    ModuleCompletion.objects.get_or_create(student=request.user, module=module)

    # Keyingi modulning 1-darsi bor bo‘lsa — o‘sha darsga
    next_module = Module.objects.filter(course=course, order__gt=module.order)\
                                .order_by("order").prefetch_related("lessons").first()
    if next_module and next_module.lessons.exists():
        first_lesson = next_module.lessons.order_by("order").first()
        messages.success(request, f"'{module.title}' yakunlandi. Keyingi modulga o‘tildi.")
        return redirect("lesson_detail", course_id=course.id, lesson_id=first_lesson.id)

    # Aks holda kurs sahifasiga — kurs tugashi mumkin
    messages.success(request, f"'{module.title}' yakunlandi. Kurs bo‘yicha barcha modullar tugallangan bo‘lishi mumkin.")
    return redirect("course_detail", course_id=course.id)

@login_required
def profile_view(request):
    enrollments = []
    for e in Enrollment.objects.filter(student=request.user):
        # shu kurs bo‘yicha so‘rov va sertifikatlarni oldindan topamiz
        cert_request = CertificateRequest.objects.filter(student=request.user, course=e.course).first()
        issued_cert = Certificate.objects.filter(student=request.user, course=e.course, status="approved").first()

        enrollments.append({
            "course": e.course,
            "progress": e.progress_percent(),
            "id": e.id,
            "cert_request": cert_request,
            "issued_cert": issued_cert
        })

    return render(request, "profile.html", {
        "enrollments": enrollments,
    })

@login_required
@require_POST
def request_certificate(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed = LessonCompletion.objects.filter(student=request.user, lesson__module__course=course).count()

    if total_lessons == 0 or completed < total_lessons:
        messages.error(request, "Avval kursni to‘liq tugatishingiz kerak!")
        return redirect("profile")

    CertificateRequest.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"‘{course.title}’ kursi uchun sertifikat arizasi topshirildi!")
    return redirect("profile")
