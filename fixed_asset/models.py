from django.db import models

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


