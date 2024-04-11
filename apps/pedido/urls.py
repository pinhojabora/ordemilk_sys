from django.urls import path
from apps.pedido.views import lista_pedido, cadastro_pedido, detalhes_pedido, editar_pedido, excluir_pedido, importar_produtos_pedido, buscar_pedido

urlpatterns = [
        path('index_pedido', lista_pedido, name='index_pedido'),
        path('cadastro_pedido', cadastro_pedido, name='cadastro_pedido'),
        path('detalhes_pedido/<int:pedido_id>/', detalhes_pedido, name='detalhes_pedido'),
        path('editar_pedido/<int:pedido_id>/', editar_pedido, name='editar_pedido'),
        path('excluir_pedido/<int:pedido_id>/', excluir_pedido, name='excluir_pedido'),
        path('importar_produtos_pedido/<int:pedido_id>/', importar_produtos_pedido, name='importar_produtos_pedido'),
        path("buscar_pedido", buscar_pedido, name="buscar_pedido"),
]
