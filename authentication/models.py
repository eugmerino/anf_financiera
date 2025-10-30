from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    dui = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        verbose_name="DUI"
    )
    photo = models.ImageField(
        upload_to='users/photos/',
        null=True,
        blank=True,
        verbose_name="Foto de perfil"
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.username}"

