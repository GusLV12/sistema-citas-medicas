from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor, Patient, User

@admin.register(User)
class UserAdminConfig(UserAdmin):
    model = User
    list_display = ("email", "role", "is_active")
    list_filter = ("role", "is_active")
    ordering = ("email",)
    fieldsets = ((None, {"fields": ("email", "password", "role", "is_active", "is_superuser", "groups", "user_permissions")}),)
    add_fieldsets = ((None, {"fields": ("email", "password1", "password2", "role")}),)
    search_fields = ("email",)

admin.site.register(Patient)
admin.site.register(Doctor)
