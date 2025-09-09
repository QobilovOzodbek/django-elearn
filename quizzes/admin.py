from django.contrib import admin
from .models import Quiz, QuizResult

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("module", "question", "correct_answer")

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("student", "quiz", "is_correct", "taken_at")
