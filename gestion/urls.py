from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_usuario, name='login'),
    path('registro/', views.registro_usuario, name='registro'), # Nueva ruta
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_usuario, name='logout'),
    path('eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('programas/', views.listar_programas, name='listar_programas'),
    path('prgramas/crear/', views.crear_programa, name='crear_programa'),
    path('fichas/', views.listar_fichas, name='listar_fichas'),
    path('fichas/crear/', views.crear_ficha, name='crear_ficha'),
    path('fichas/eliminar/<str:id>/', views.eliminar_ficha, name='eliminar_ficha'),
    path('fichas/editar/<str:id>/', views.editar_ficha, name='editar_ficha'),
]