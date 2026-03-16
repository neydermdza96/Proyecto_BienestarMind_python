from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Usuario, Roles, UsuarioRoles
from django.db import transaction

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

# --- REGISTRO ---
def registro_usuario(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        documento = request.POST.get('documento') 
        correo = request.POST.get('correo')
        genero = request.POST.get('genero')
        telefono = request.POST.get('telefono')
        fecha_nac = request.POST.get('fecha_nacimiento')
        clave = request.POST.get('password')
        id_rol_elegido = request.POST.get('rol')

        try:
            with transaction.atomic():
                if User.objects.filter(username=documento).exists():
                    messages.error(request, "Este documento ya está registrado.")
                    return redirect('registro')
                
                User.objects.create_user(
                    username=documento, 
                    email=correo, 
                    password=clave,
                    first_name=nombres,
                    last_name=apellidos
                )

                nuevo_usuario = Usuario.objects.create(
                    nombres=nombres,
                    apellidos=apellidos,
                    documento=documento,
                    correo=correo,
                    genero=genero,
                    telefono=telefono,
                    fecha_de_nacimiento=fecha_nac,
                    contrasena=clave 
                )

                rol_obj = Roles.objects.get(id_rol=id_rol_elegido)
                UsuarioRoles.objects.create(
                    id_usuario=nuevo_usuario,
                    id_rol=rol_obj
                )

                messages.success(request, f"Usuario {nombres} registrado con éxito.")
                return redirect('login')

        except Exception as e:
            messages.error(request, f"Error al registrar: {e}")
            
    roles = Roles.objects.all()
    return render(request, 'gestion/registro.html', {'roles': roles})

# --- DASHBOARD ---
@login_required
def dashboard(request):
    usuarios_con_roles = UsuarioRoles.objects.select_related('id_usuario', 'id_rol').all()
    context = {
        'usuarios_roles': usuarios_con_roles
    }
    return render(request, 'gestion/dashboard.html', context)

# --- LOGOUT ---
def logout_usuario(request):
    logout(request)
    return redirect('inicio')

# --- ELIMINAR (CORREGIDO PARA EVITAR ERROR DE LLAVE FORÁNEA) ---
def eliminar_usuario(request, id):
    try:
        with transaction.atomic():
            # 1. Buscamos el usuario en tu tabla personalizada
            usuario_db = Usuario.objects.get(id_usuario=id)
            doc_usuario = usuario_db.documento
            
            # 2. Borramos primero la relación en UsuarioRoles
            UsuarioRoles.objects.filter(id_usuario=id).delete()
            
            # 3. Borramos al usuario de tu tabla de PostgreSQL
            usuario_db.delete()
            
            # 4. También borramos al usuario del sistema de autenticación de Django (User)
            # Para que no pueda volver a entrar si ya lo borraste del sistema
            User.objects.filter(username=doc_usuario).delete()
            
            messages.success(request, "Usuario y sus permisos eliminados correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar: {e}")
    
    return redirect('dashboard')

def editar_usuario(request, id):
    usuario = Usuario.objects.get(id_usuario=id)
    roles = Roles.objects.all()
    # Obtenemos el rol actual del usuario
    rol_actual = UsuarioRoles.objects.filter(id_usuario=id).first()
    
    if request.method == 'POST':
        # Actualizamos los datos del modelo Usuario
        usuario.nombres = request.POST.get('nombres')
        usuario.apellidos = request.POST.get('apellidos')
        usuario.correo = request.POST.get('correo')
        usuario.telefono = request.POST.get('telefono')
        usuario.genero = request.POST.get('genero')
        usuario.save()
        
        # Actualizamos el Rol en UsuarioRoles
        nuevo_rol_id = request.POST.get('rol')
        nuevo_rol = Roles.objects.get(id_rol=nuevo_rol_id)
        
        if rol_actual:
            rol_actual.id_rol = nuevo_rol
            rol_actual.save()
            
        messages.success(request, f"Usuario {usuario.nombres} actualizado correctamente.")
        return redirect('dashboard')

    return render(request, 'gestion/editar_usuario.html', {
        'usuario': usuario,
        'roles': roles,
        'rol_actual': rol_actual
    })