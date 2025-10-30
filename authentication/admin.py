from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('dui', 'photo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('dui', 'photo')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'dui', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'dui')

