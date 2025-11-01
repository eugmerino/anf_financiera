from django.db import models, transaction
from django.db.models import Max

# Create your models here.
class Institution(models.Model):
    code = models.CharField(
        max_length=4,
        unique=True,
        verbose_name="Código de la institución"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre de la institución",
        null=False,
        blank=False
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Dirección",
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"
        
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def set_code(self):
        """
        Set the code for the institution.
        This method can be customized to generate a code based on specific rules.
        """
        if not self.code:
            # Example logic to generate a code
            self.code = f"{self.id:04d}"  # Example format: 0001

    def save(self, *args, **kwargs):
        # Primero guarda para obtener el ID si aún no existe
        creating = self.pk is None
        super().save(*args, **kwargs)
        
        # Si se acaba de crear, genera el código y guarda de nuevo
        if creating and not self.code:
            self.set_code()
            super().save(update_fields=["code"])

class Department(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre del departamento",
        null=False,
        blank=False
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="departments",
        verbose_name="Institución"
    )
    # Lo dejamos opcional en el modelo para poder autogenerarlo en save()
    code = models.CharField(
        max_length=4,
        verbose_name="Código del departamento",
        null=True,
        blank=True,
        help_text="Se autogenera por institución como 0001, 0002, ..."
    )
    description = models.TextField(
        verbose_name="Descripción del departamento",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "code"],
                name="uniq_department_institution_code"
            )
        ]
        indexes = [
            models.Index(fields=["institution", "code"]),
        ]

    def __str__(self):
        inst_code = self.institution.code if self.institution_id else "----"
        dept_code = self.code or "----"
        return f"{dept_code}-{inst_code} - {self.name}"

    def _next_code_for_institution(self) -> str:
        """
        Obtiene el siguiente código de 4 dígitos para la institución dada.
        Busca el código máximo existente (como cadena), lo convierte a int
        y suma 1. Si no hay registros, retorna '0001'.
        """
        # Tomamos el máximo código actual para esa institución
        max_code = (
            Department.objects
            .filter(institution=self.institution)
            .aggregate(mx=Max("code"))
            .get("mx")
        )

        if not max_code:
            return "0001"

        try:
            nxt = int(max_code) + 1
        except ValueError:
            # Si por alguna razón el código máximo no es numérico, reiniciamos.
            nxt = 1

        # Aseguramos 4 dígitos, cortando a 4 si se excede (raro, pero seguro)
        return f"{nxt:04d}"[:4]

    def save(self, *args, **kwargs):
        # Usamos una transacción para evitar condiciones de carrera
        with transaction.atomic():
            creating = self.pk is None
            if creating and not self.code:
                # Bloqueo lógico: recalculamos dentro de la transacción
                self.code = self._next_code_for_institution()
            super().save(*args, **kwargs)


