from django.urls import path
from apps.galeria.views import index_galeria, nova_imagem, imagem, editar_imagem, excluir_imagem
 
urlpatterns = [
        path('index_galeria', index_galeria, name='index_galeria'),
        path('nova-imagem', nova_imagem, name='nova_imagem'),
        path('imagem/<int:foto_id>/', imagem, name='imagem'),
        path('editar_imagem/<int:foto_id>/', editar_imagem, name='editar_imagem'),
        path('excluir_imagem/<int:foto_id>/', excluir_imagem, name='excluir_imagem'),
]
