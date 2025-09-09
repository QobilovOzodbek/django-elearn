from django.contrib import admin
from .models import CertificateRequest, Certificate

@admin.register(CertificateRequest)
class CertificateRequestAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "status", "date_requested")
    list_filter = ("status", "course")
    search_fields = ("student__username", "course__title")

    actions = ["approve_requests", "reject_requests"]

    @admin.action(description="✅ Arizani tasdiqlash")
    def approve_requests(self, request, queryset):
        updated = queryset.filter(status="pending").update(status="approved")
        self.message_user(request, f"{updated} ta ariza tasdiqlandi. Endi sertifikat qo‘lda yuklanishi kerak.")

    @admin.action(description="❌ Arizani rad etish")
    def reject_requests(self, request, queryset):
        updated = queryset.filter(status="pending").update(status="rejected")
        self.message_user(request, f"{updated} ta ariza rad etildi.")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "status", "issued_at")
    list_filter = ("status",)
    search_fields = ("student__username", "course__title")
