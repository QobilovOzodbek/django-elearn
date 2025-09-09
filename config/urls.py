from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("courses.urls")),       # bosh sahifa endi kurslar bo‘ladi
    path('', include("users.urls")),         # login/register/profil
    path('', include("certificates.urls")),  # sertifikatlar
]

# Faqat DEBUG=True bo‘lsa ishlaydi (development rejimida)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
