from django.db import models
from users.models import User
from django.conf import settings
from urllib.parse import urlparse, parse_qs

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey("Module", related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]

    def embed_url(self):
        """
        YouTube URL’ni barcha hollarda embed formatga o‘giradi.
        Playlist parametrlari (`list`, `index`) saqlanadi.
        """
        if not self.video_url:
            return ""

        url_data = urlparse(self.video_url)

        # query parametrlardan olish (youtube.com/watch?v=...)
        if "youtube.com" in url_data.netloc:
            query = parse_qs(url_data.query)
            video_id = query.get("v", [None])[0]
            playlist_id = query.get("list", [None])[0]
            index = query.get("index", [None])[0]

        # qisqa format (youtu.be/VIDEO_ID)
        elif "youtu.be" in url_data.netloc:
            path_parts = url_data.path.strip("/").split("/")
            video_id = path_parts[-1] if path_parts else None
            query = parse_qs(url_data.query)
            playlist_id = query.get("list", [None])[0]
            index = query.get("index", [None])[0]

        else:
            return self.video_url  # fallback

        if not video_id:
            return self.video_url

        # embed link quramiz
        embed = f"https://www.youtube.com/embed/{video_id}"
        params = []
        if playlist_id:
            params.append(f"list={playlist_id}")
        if index:
            params.append(f"index={index}")

        if params:
            embed += "?" + "&".join(params)

        return embed
    
class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def total_lessons(self):
        from .models import Lesson
        return Lesson.objects.filter(module__course=self.course).count()

    def completed_lessons(self):
        from .models import LessonCompletion
        return LessonCompletion.objects.filter(
            student=self.student,
            lesson__module__course=self.course
        ).count()

    def progress_percent(self):
        total = self.total_lessons()
        done = self.completed_lessons()
        return int(done * 100 / total) if total else 0

    def __str__(self):
        return f"{self.student} -> {self.course}"

class LessonCompletion(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} - {self.lesson}"

class ModuleCompletion(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'module')

    def __str__(self):
        return f"{self.student} - {self.module}"
    

