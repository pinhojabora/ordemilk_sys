from django.urls import path
from apps.carrinho.views import(
                                adicionar_carrinho,
                                lista_carrinho,
                                excluir_item_carrinho,
                                editar_carrinho,
                                limpar_carrinho
)
 
urlpatterns = [
    path('index_carrinho/', lista_carrinho, name='lista_carrinho'),  
    path('adicionar_carrinho/', adicionar_carrinho, name='adicionar_carrinho'),
    path('excluir_item/<int:carrinho_id>/', excluir_item_carrinho, name='excluir_item_carrinho'),
    path('editar_carrinho/<int:carrinho_id>/', editar_carrinho, name='editar_carrinho'),
    path('limpar_carrinho', limpar_carrinho, name='limpar_carrinho')
]
