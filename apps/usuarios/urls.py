from django.urls import path
from apps.usuarios.views import index_usuario, login, cadastro, logout
 
urlpatterns = [
        path('index_usuario', index_usuario, name='index_usuario'),
        path('login', login, name='login'),
        path('cadastro', cadastro, name='cadastro'),
        path('logout', logout, name='logout')
        
]
