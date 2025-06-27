from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Perfil

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Crea automáticamente un Perfil cada vez que se registra un nuevo User.
    """
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_migrate)
def crear_superusuario_por_defecto(sender, **kwargs):
    """
    Tras aplicar migraciones, si no existe un superusuario 'admin', lo crea con contraseña 'admin123'.
    """
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
