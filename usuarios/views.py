from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import RegistroForm, LoginForm, PerfilForm, UsuarioPerfilForm
from .models import Perfil
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UsuarioAdminForm
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from .models import JuegoFavorito


RAWG_API_KEY = 'cd63501d89c844d7aee3e52140a8676a'

@login_required
def recomendacion_videojuegos(request):
    query = request.GET.get('q', '')
    genero = request.GET.get('genero', '')
    page = request.GET.get('page', '1')

    url = f'https://api.rawg.io/api/games?key={RAWG_API_KEY}&page={page}&page_size=9'
    if query:
        url += f'&search={query}'
    if genero:
        url += f'&genres={genero}'

    response = requests.get(url)
    juegos = response.json().get('results', []) if response.status_code == 200 else []

    if request.method == 'POST':
        juego_id = request.POST.get('juego_id')
        nombre = request.POST.get('nombre')
        imagen = request.POST.get('imagen')
        if not JuegoFavorito.objects.filter(user=request.user, juego_id=juego_id).exists():
            JuegoFavorito.objects.create(user=request.user, juego_id=juego_id, nombre=nombre, imagen=imagen)

    return render(request, 'usuarios/recomendacion.html', {
        'juegos': juegos,
        'query': query,
        'genero': genero,
        'page': int(page)
    })

@login_required
def mis_favoritos(request):
    favoritos = JuegoFavorito.objects.filter(user=request.user).order_by('-fecha_guardado')
    return render(request, 'usuarios/favoritos.html', {'favoritos': favoritos})

@login_required
def inicio(request):
    url = f'https://api.rawg.io/api/games?key={RAWG_API_KEY}&ordering=-added&page_size=6'
    response = requests.get(url)
    juegos = response.json().get('results', []) if response.status_code == 200 else []
    return render(request, 'usuarios/inicio.html', {'juegos': juegos})


@staff_member_required
def gestionar_usuarios(request):
    usuarios = User.objects.all()

    if request.method == 'POST':
        print("POST recibido:", request.POST)

        if 'crear' in request.POST:
            form = UsuarioAdminForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Usuario creado correctamente.")
                return redirect('gestionar_usuarios')
            else:
                messages.error(request, "Error al crear usuario.")

        elif 'editar_id' in request.POST:
            try:
                user = User.objects.get(id=request.POST['editar_id'])
                form = UsuarioAdminForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Usuario actualizado correctamente.")
                    return redirect('gestionar_usuarios')
                else:
                    messages.error(request, "Error al actualizar usuario.")
            except User.DoesNotExist:
                messages.error(request, "Usuario no encontrado.")

        elif 'eliminar_id' in request.POST:
            try:
                user = User.objects.get(id=request.POST['eliminar_id'])
                user.delete()
                messages.success(request, "Usuario eliminado correctamente.")
                return redirect('gestionar_usuarios')
            except User.DoesNotExist:
                messages.error(request, "Usuario no encontrado.")

    else:
        form = UsuarioAdminForm()

    return render(request, 'usuarios/gestionar_usuarios.html', {
        'usuarios': usuarios,
        'form': form
    })


@login_required
def editar_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        usuario_form = UsuarioPerfilForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)

        # Solo crea el password_form si se intenta cambiar la contraseña
        if any(request.POST.get(field) for field in ['old_password', 'new_password1', 'new_password2']):
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            cambiar_contraseña = True
        else:
            password_form = None
            cambiar_contraseña = False

        if usuario_form.is_valid() and perfil_form.is_valid():
            if cambiar_contraseña:
                if password_form.is_valid():
                    password_form.save()
                    update_session_auth_hash(request, password_form.user)
                else:
                    # Si la contraseña no es válida, renderiza con errores
                    return render(request, 'usuarios/editar_perfil.html', {
                        'usuario_form': usuario_form,
                        'perfil_form': perfil_form,
                        'password_form': password_form,
                    })
            usuario_form.save()
            perfil_form.save()
            return redirect('inicio')

    else:
        usuario_form = UsuarioPerfilForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'usuarios/editar_perfil.html', {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form,
        'password_form': password_form,
    })


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('login')


