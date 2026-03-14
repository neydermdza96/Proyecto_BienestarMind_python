from django.contrib import admin
from .models import Usuario, Ficha, Roles, Sede, Programas, Asesoria, Elementos, Espacios

# Una forma más pro de registrar el modelo Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombres', 'apellidos', 'documento', 'correo') # Columnas que verás en la lista
    search_fields = ('nombres', 'documento') # Barra de búsqueda por nombre o cédula

# Registro sencillo para los demás
admin.site.register(Ficha)
admin.site.register(Roles)
admin.site.register(Sede)
admin.site.register(Programas)
admin.site.register(Asesoria)
admin.site.register(Elementos)
admin.site.register(Espacios)