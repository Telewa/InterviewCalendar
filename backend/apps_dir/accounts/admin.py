from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("user_type", "id",)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    list_filter = UserAdmin.list_filter + ("user_type",)


admin.site.register(User, CustomUserAdmin)
