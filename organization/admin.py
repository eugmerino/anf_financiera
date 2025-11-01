from django.contrib import admin
from django import forms
from .models import Institution, Department

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

    def get_fields(self, request, obj=None):
        # Al crear: no mostramos 'code'
        if obj is None:
            return ("name", "address")

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


class DepartmentAdminForm(forms.ModelForm):
    class Meta:
        model = Department
        # Excluimos el campo 'code' porque se genera automáticamente
        fields = ["institution", "name", "description"]

class DepartmentAdmin(admin.ModelAdmin):
    form = DepartmentAdminForm
    list_display = ("full_code", "name", "institution", "description")
    list_filter = ("institution",)
    search_fields = ("code", "name", "institution__name")
    ordering = ("institution__code", "code")

    def full_code(self, obj):
        """Muestra el código completo Institución-Departamento en la lista."""
        return f"{obj.institution.code}-{obj.code}"
    full_code.short_description = "Código completo"

    def get_fields(self, request, obj=None):
        # Al crear: no mostramos el código
        if obj is None:
            return ("institution", "name", "description")
        
        return ("institution", "code", "name", "description")

    def save_model(self, request, obj, form, change):
        creating = obj.pk is None
        # Guardamos para obtener ID y asignar institución
        super().save_model(request, obj, form, change)
        # Si es nuevo y no tiene código, lo generamos
        if creating and not obj.code:
            obj.code = obj._next_code_for_institution()
            obj.save(update_fields=["code"])

admin.site.register(Department, DepartmentAdmin)