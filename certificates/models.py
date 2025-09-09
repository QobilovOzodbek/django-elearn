from django.db import models
from users.models import User
from courses.models import Course

class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to="certificates/")
    issued_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending','Kutilmoqda'),('approved','Tasdiqlandi')],
        default='pending'
    )

    def __str__(self):
        return f"Sertifikat - {self.student.username} - {self.course.title}"

class CertificateRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificate_requests")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Ko‘rib chiqilmoqda"), ("approved", "Tasdiqlangan"), ("rejected", "Rad etilgan")],
        default="pending"
    )

    def __str__(self):
        return f"{self.student.username} - {self.course.title} ({self.status})"
