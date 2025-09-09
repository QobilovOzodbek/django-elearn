from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # qo‘shimcha maydonlar qo‘shishingiz mumkin
    role = models.CharField(
        max_length=20,
        choices=[("student", "Talaba"), ("teacher", "O‘qituvchi"), ("admin", "Admin")],
        default="student"
    )
    ofile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.username
