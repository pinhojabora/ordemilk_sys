from django.urls import path
from apps.lista.views import lista_precos, cadastro_lista

urlpatterns = [
        path('lista_precos/', lista_precos, name='lista_precos'),
        path('cadastro_lista/', cadastro_lista, name='cadastro_lista'),

        
]
