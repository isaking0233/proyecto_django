from django.db import models
from django.contrib.auth.models import User


class JuegoFavorito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    juego_id = models.IntegerField()
    nombre = models.CharField(max_length=255)
    imagen = models.URLField()
    fecha_guardado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.user.username}"

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='perfiles/', default='perfiles/default.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'
