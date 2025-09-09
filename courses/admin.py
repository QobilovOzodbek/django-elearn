from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, LessonCompletion, ModuleCompletion

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "video_url", "order", "module")
    list_filter = ("module",)
    search_fields = ("title",)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "course", "progress_percent", "date_enrolled")
    def progress_percent(self, obj):
        return f"{obj.progress_percent()}%"
    
@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "lesson", "completed_at")
    list_filter = ("student", "lesson__module__course")

@admin.register(ModuleCompletion)
class ModuleCompletionAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "module", "completed_at")
    list_filter = ("student", "module__course")
