# admin.py
from django.contrib import admin
from django import forms
from .models import Institution

class InstitutionAdminForm(forms.ModelForm):
    class Meta:
        model = Institution
        # No pedimos 'code' al crear
        fields = ["name", "address"]

class InstitutionAdmin(admin.ModelAdmin):
    form = InstitutionAdminForm
    list_display = ("code", "name", "address")
    search_fields = ("code", "name", "address")
    ordering = ("code",)
    readonly_fields = ("code",)  # visible solo al editar (como solo lectura)
    # Nota: como el form no incluye 'code', no aparecerá al crear

    def get_fields(self, request, obj=None):
        # Al crear: no mostramos 'code'
        if obj is None:
            return ("name", "address")
        # Al editar: lo mostramos como readonly
        return ("code", "name", "address")

    def save_model(self, request, obj, form, change):
        creating = obj.pk is None
        # 1) guardamos primero para obtener el ID
        super().save_model(request, obj, form, change)
        # 2) si es nuevo y no hay code, lo generamos
        if creating and not obj.code:
            obj.set_code()
            obj.save(update_fields=["code"])

admin.site.register(Institution, InstitutionAdmin)
