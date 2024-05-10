from django.urls import path
from apps.produto.views import(
                                lista_produto, 
                                detalhes_produto, 
                                cadastro_produto, 
                                buscar, editar_produto, 
                                lista_preco, 
                                lista_categoria, 
                                lista_subcategoria, 
                                cadastro_categoria, 
                                cadastro_subcategoria,
                                editar_categoria,
                                excluir_categoria,
                                editar_subcategoria,
                                excluir_subcategoria,
                                importar_preco,
                                importar_componentes,
                                importar_componentes2
                                
)
 
urlpatterns = [
        path('produto', lista_produto, name='produto'),
        path('produto/<int:produto_id>/', detalhes_produto, name='detalhes_produto'),
        path('cadastro_produto', cadastro_produto, name='cadastro_produto'),
        path("buscar", buscar, name="buscar"),
        path('editar_produto/<int:produto_id>/', editar_produto, name='editar_produto'),
        path('lista_preco', lista_preco, name='lista_preco'),
        path('categoria', lista_categoria, name='categoria'),
        path('cadastro_categoria', cadastro_categoria, name='cadastro_categoria'),
        path('subcategoria', lista_subcategoria, name='subcategoria'),
        path('cadastro_subcategoria', cadastro_subcategoria, name='cadastro_subcategoria'),
        path('editar_categoria/<int:categoria_id>/', editar_categoria, name='editar_categoria'),
        path('excluir_categoria/<int:categoria_id>/', excluir_categoria, name='excluir_categoria'),
        path('editar_subcategoria/<int:subcategoria_id>/', editar_subcategoria, name='editar_subcategoria'),
        path('excluir_subcategoria/<int:subcategoria_id>/', excluir_subcategoria, name='excluir_subcategoria'),
        path('importar_preco/', importar_preco, name='importar_preco'),
        path('importar_componentes/', importar_componentes, name='importar_componentes'),
        path('importar_componentes2/', importar_componentes2, name='importar_componentes2'),
]
