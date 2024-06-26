from django.urls import path
from apps.orcamento.views import (
    lista_orcamento, 
    cadastro_orcamento, 
    detalhes_orcamento,
    editar_orcamento, 
    cadastro_item_orcamento, 
    editar_item_orcamento, 
    excluir_item_orcamento, 
    editar_entrada_orcamento, 
    adicionar_parcela, 
    editar_parcela, 
    excluir_parcela,
    converter_orcamento_pedido,
    excluir_orcamento,
    importar_produtos,
    buscar_orcamento,
    carrinho_vazio,
    imprimir_orcamento_pdf,
    atualizar_valor_orcamento
    )

urlpatterns = [
        path('index_orcamento', lista_orcamento, name='index_orcamento'),
        path('cadastro_orcamento', cadastro_orcamento, name='cadastro_orcamento'),
        path('detalhes_orcamento/<int:orcamento_id>/', detalhes_orcamento, name='detalhes_orcamento'),
        path('editar_orcamento/<int:orcamento_id>/', editar_orcamento, name='editar_orcamento'),
        path('orcamento/<int:orcamento_id>/cadastro-item/', cadastro_item_orcamento, name='cadastro_item_orcamento'),
        path('editar-item-orcamento/<int:item_id>/', editar_item_orcamento, name='editar_item_orcamento'),
        path('excluir-item-orcamento/<int:item_id>/', excluir_item_orcamento, name='excluir_item_orcamento'),
        path('editar_entrada_orcamento/<int:orcamento_id>/', editar_entrada_orcamento, name='editar_entrada_orcamento'),
        path('adicionar_parcela/<int:orcamento_id>/', adicionar_parcela, name='adicionar_parcela'),
        path('editar_parcela/<int:parcela_id>/', editar_parcela, name='editar_parcela'),
        path('excluir_parcela/<int:parcela_id>/', excluir_parcela, name='excluir_parcela'),
        path('converter_orcamento_para_pedido/<int:orcamento_id>/', converter_orcamento_pedido, name='converter_orcamento_para_pedido'),
        path('excluir_orcamento/<int:orcamento_id>/', excluir_orcamento, name='excluir_orcamento'),
        path('importar_produtos/<int:orcamento_id>/', importar_produtos, name='importar_produtos'),
        path("buscar_orcamento", buscar_orcamento, name="buscar_orcamento"),
        path('carrinho_vazio', carrinho_vazio, name='carrinho_vazio'),
        path('imprimir_orcamento/<int:orcamento_id>/pdf/', imprimir_orcamento_pdf, name='imprimir_orcamento_pdf'),
        path('atualizar_valor_orcamento/<int:orcamento_id>/', atualizar_valor_orcamento, name='atualizar_valor_orcamento'),
]
