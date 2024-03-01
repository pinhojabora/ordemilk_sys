from django.urls import path
from apps.produto.views import lista_produto, detalhes_produto, cadastro_produto, buscar
 
urlpatterns = [
        path('produto', lista_produto, name='produto'),
        path('produto/<int:produto_id>/', detalhes_produto, name='detalhes_produto'),
        path('cadastro_produto', cadastro_produto, name='cadastro_produto'),
        path("buscar", buscar, name="buscar"),
]
