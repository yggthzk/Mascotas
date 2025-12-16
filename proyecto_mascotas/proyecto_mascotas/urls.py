from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.lista_mascotas, name='lista_mascotas'),
    path('crear/', views.crear_mascota, name='crear_mascota'),
    path('buscar/', views.buscar_mascota, name='buscar_mascota'),
    path('eliminar/<int:id>/', views.eliminar_mascota, name='eliminar_mascota'),
    path('editar/<int:id>/', views.editar_mascota, name='editar_mascota'),
    path('api/chatbot/', views.api_chatbot, name='api_chatbot'),
]