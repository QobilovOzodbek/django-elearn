# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User   # custom User model
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Foydalanuvchi nomi",
            "email": "Email",
            "password1": "Parol",
            "password2": "Parolni tasdiqlang",
        }
        help_texts = {  # unnecessary help_text larni olib tashlash
            "username": None,
            "email": None,
            "password1": None,
            "password2": None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label
            })

