from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from courses.models import Enrollment
from certificates.models import Certificate
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # parolni xeshlash
            user.save()
            login(request, user)  # avtomatik login
            return redirect("home")  # ro‘yxatdan o‘tgandan keyin asosiy sahifa
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})

# Kirish
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Xush kelibsiz!")
            return redirect("profile")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# Chiqish
def logout_view(request):
    logout(request)
    messages.info(request, "Chiqdingiz.")
    return redirect("login")

# Profil
@login_required
def profile_view(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    certificates = Certificate.objects.filter(student=request.user)
    return render(request, "profile.html", {
        "enrollments": enrollments,
        "certificates": certificates
    })
