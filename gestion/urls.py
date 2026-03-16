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
]