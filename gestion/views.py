from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from .models import Usuario, Roles, UsuarioRoles, Programas, Ficha, UsuarioFicha

# --- INICIO ---
def inicio(request):
    return render(request, 'gestion/inicio.html')

# --- LOGIN ---
def login_usuario(request):
    if request.method == 'POST':
        usuario_doc = request.POST.get('username')
        clave = request.POST.get('password')
        user = authenticate(request, username=usuario_doc, password=clave) 
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Documento o contraseña incorrectos")
    return render(request, 'gestion/login.html')

# --- DASHBOARD (SOLUCIÓN MAESTRA PARA PERMISOS) ---
@login_required
def dashboard(request):
    # Si eres superusuario de consola O tienes el rol ADMINISTRADOR, es_admin = True
    es_admin = False
    if request.user.is_superuser:
        es_admin = True
    else:
        rol_rel = UsuarioRoles.objects.filter(id_usuario__documento=request.user.username).first()
        if rol_rel and (rol_rel.id_rol.descripcion == 'ADMINISTRADOR' or rol_rel.id_rol.id_rol == 1):
            es_admin = True

    usuarios = Usuario.objects.all()
    user_roles = UsuarioRoles.objects.select_related('id_rol').all()
    user_fichas = UsuarioFicha.objects.select_related('id_ficha').all()
    
    context = {
        'usuarios': usuarios,
        'user_roles': user_roles,
        'user_fichas': user_fichas,
        'es_admin': es_admin, 
    }
    return render(request, 'gestion/dashboard.html', context)

# --- REGISTRO USUARIO ---
def registro_usuario(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        documento = request.POST.get('documento') 
        correo = request.POST.get('correo')
        clave = request.POST.get('password')
        id_rol_elegido = request.POST.get('rol')
        id_ficha_elegida = request.POST.get('ficha')

        try:
            with transaction.atomic():
                User.objects.create_user(username=documento, email=correo, password=clave, first_name=nombres, last_name=apellidos)
                nuevo_usuario = Usuario.objects.create(
                    nombres=nombres, apellidos=apellidos, documento=documento, 
                    correo=correo, contrasena=clave, genero=request.POST.get('genero'),
                    telefono=request.POST.get('telefono'), fecha_de_nacimiento=request.POST.get('fecha_nacimiento')
                )
                rol_obj = Roles.objects.get(id_rol=id_rol_elegido)
                UsuarioRoles.objects.create(id_usuario=nuevo_usuario, id_rol=rol_obj)
                if id_ficha_elegida:
                    ficha_obj = Ficha.objects.get(id_ficha=id_ficha_elegida)
                    UsuarioFicha.objects.create(id_usuario=nuevo_usuario, id_ficha=ficha_obj)
                
                messages.success(request, "Usuario creado con éxito")
                return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            
    return render(request, 'gestion/registro.html', {'roles': Roles.objects.all(), 'fichas': Ficha.objects.all()})

# --- ELIMINAR USUARIO ---
def eliminar_usuario(request, id):
    rol_rel = UsuarioRoles.objects.filter(id_usuario__documento=request.user.username).first()
    if request.user.is_superuser or (rol_rel and rol_rel.id_rol.id_rol == 1):
        try:
            with transaction.atomic():
                usuario_db = Usuario.objects.get(id_usuario=id)
                doc = usuario_db.documento
                UsuarioRoles.objects.filter(id_usuario=id).delete()
                UsuarioFicha.objects.filter(id_usuario=id).delete()
                usuario_db.delete()
                User.objects.filter(username=doc).delete()
                messages.success(request, "Usuario eliminado")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return redirect('dashboard')

# --- EDITAR USUARIO ---
def editar_usuario(request, id):
    usuario = Usuario.objects.get(id_usuario=id)
    if request.method == 'POST':
        usuario.nombres = request.POST.get('nombres')
        usuario.apellidos = request.POST.get('apellidos')
        usuario.correo = request.POST.get('correo')
        usuario.save()
        messages.success(request, "Usuario actualizado")
        return redirect('dashboard')
    return render(request, 'gestion/editar_usuario.html', {'usuario': usuario, 'roles': Roles.objects.all()})

# --- GESTIÓN DE PROGRAMAS (RESTAURADO) ---
@login_required
def listar_programas(request):
    programas = Programas.objects.prefetch_related('ficha_set').all()
    return render(request, 'gestion/programas.html', {'programas': programas})

@login_required
def crear_programa(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_programa')
        Programas.objects.create(nombre_programa=nombre)
        messages.success(request, "Programa creado correctamente")
        return redirect('listar_programas')
    return render(request, 'gestion/crear_programa.html')

# --- GESTIÓN DE FICHAS (RESTAURADO) ---
@login_required
def listar_fichas(request):
    fichas = Ficha.objects.select_related('id_programa').all()
    return render(request, 'gestion/fichas.html', {'fichas': fichas})

@login_required
def crear_ficha(request):
    if request.method == 'POST':
        id_f = request.POST.get('numero_ficha')
        Ficha.objects.create(
            id_ficha=id_f,
            descripcion=request.POST.get('descripcion'),
            jornada_ficha=request.POST.get('jornada'),
            id_programa=Programas.objects.get(id_programa=request.POST.get('programa'))
        )
        messages.success(request, f"Ficha {id_f} creada")
        return redirect('listar_fichas')
    return render(request, 'gestion/crear_ficha.html', {'programas': Programas.objects.all()})

@login_required
def editar_ficha(request, id):
    ficha = Ficha.objects.get(id_ficha=id)
    if request.method == 'POST':
        ficha.descripcion = request.POST.get('descripcion')
        ficha.jornada_ficha = request.POST.get('jornada')
        ficha.id_programa = Programas.objects.get(id_programa=request.POST.get('programa'))
        ficha.save()
        messages.success(request, "Ficha actualizada")
        return redirect('listar_fichas')
    return render(request, 'gestion/editar_ficha.html', {'ficha': ficha, 'programas': Programas.objects.all()})

def eliminar_ficha(request, id):
    try:
        with transaction.atomic():
            # 1. Borramos primero las vinculaciones de los usuarios con esta ficha
            # Esto quita el "amarre" que causa el error de llave foránea
            UsuarioFicha.objects.filter(id_ficha=id).delete()
            
            # 2. Ahora que no hay nadie amarrado, borramos la ficha tranquila mente
            Ficha.objects.filter(id_ficha=id).delete()
            
            messages.success(request, f"Ficha {id} eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la ficha: {e}")
    
    return redirect('listar_fichas')

# --- LOGOUT ---
def logout_usuario(request):
    logout(request)
    return redirect('inicio')