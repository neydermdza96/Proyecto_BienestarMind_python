# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'roles'
    
    def __str__(self):
        return self.descripcion

class Permisos(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'permisos'

class RolesPermisos(models.Model):
    id_roles_permisos = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='id_rol')
    id_permiso = models.ForeignKey(Permisos, models.DO_NOTHING, db_column='id_permiso')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'roles_permisos'

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    documento = models.CharField(max_length=20)
    correo = models.CharField(max_length=100)
    genero = models.CharField(max_length=15)
    telefono = models.CharField(max_length=20)
    fecha_de_nacimiento = models.DateField()
    contrasena = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class UsuarioRoles(models.Model):
    id_usuario_roles = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_rol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='id_rol')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'usuario_roles'

class Sede(models.Model):
    id_sede = models.AutoField(primary_key=True)
    nombre_sede = models.CharField(max_length=100)
    telefono_sede = models.CharField(max_length=20)
    direccion_sede = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'sede'

    def __str__(self):
        return self.nombre_sede

class Programas(models.Model):
    id_programa = models.AutoField(primary_key=True)
    nombre_programa = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'programas'

    def __str__(self):
        return self.nombre_programa

class Ficha(models.Model):
    id_ficha = models.CharField(primary_key=True, max_length=20)
    descripcion = models.CharField(max_length=255)
    jornada_ficha = models.CharField(max_length=50)
    id_programa = models.ForeignKey(Programas, models.DO_NOTHING, db_column='id_programa')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'ficha'

    def __str__(self):
        return f"{self.id_ficha} - {self.descripcion}"

class UsuarioFicha(models.Model):
    id_usuario_ficha = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_ficha = models.ForeignKey(Ficha, models.DO_NOTHING, db_column='id_ficha')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'usuario_ficha'

class Asesoria(models.Model):
    id_asesoria = models.AutoField(primary_key=True)
    motivo_asesoria = models.CharField(max_length=255)
    fecha = models.DateField()
    id_usuario_recibe = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario_recibe')
    id_usuario_asesor = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario_asesor', related_name='asesoria_asesor_set')
    ficha_id_ficha = models.ForeignKey(Ficha, models.DO_NOTHING, db_column='ficha_id_ficha', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'asesoria'

class CategoriaElementos(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'categoria_elementos'

    def __str__(self):
        return self.descripcion

class Elementos(models.Model):
    id_elemento = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(CategoriaElementos, models.DO_NOTHING, db_column='id_categoria')
    nombre_elemento = models.CharField(max_length=100)
    estado_elemento = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'elementos'

    def __str__(self):
        return self.nombre_elemento

class Espacios(models.Model):
    id_espacio = models.AutoField(primary_key=True)
    id_sede = models.ForeignKey(Sede, models.DO_NOTHING, db_column='id_sede')
    nombre_del_espacio = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'espacios'

    def __str__(self):
        return self.nombre_del_espacio

class Reservaelementos(models.Model):
    id_reservaelemento = models.AutoField(primary_key=True)
    fecha_reserva = models.DateField()
    descripcion_reserva = models.CharField(max_length=255)
    id_ficha = models.ForeignKey(Ficha, models.DO_NOTHING, db_column='id_ficha', blank=True, null=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_elemento = models.ForeignKey(Elementos, models.DO_NOTHING, db_column='id_elemento', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'reservaelementos'

class Reservaespacios(models.Model):
    id_reservaespacio = models.AutoField(primary_key=True)
    fecha_reserva = models.DateField()
    motivo_reserva = models.CharField(max_length=255)
    id_ficha = models.ForeignKey(Ficha, models.DO_NOTHING, db_column='id_ficha')
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_espacio = models.ForeignKey(Espacios, models.DO_NOTHING, db_column='id_espacio')
    duracion = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'reservaespacios'
