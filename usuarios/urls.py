from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),
    path('usuarios/gestionar/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('recomendaciones/', views.recomendacion_videojuegos, name='recomendacion_videojuegos'),
    path('favoritos/', views.mis_favoritos, name='mis_favoritos'),
    path('cambiar-contraseña/', auth_views.PasswordChangeView.as_view(
        template_name='usuarios/cambiar_contraseña.html',
        success_url='/perfil/'
    ), name='cambiar_contraseña'),
]
