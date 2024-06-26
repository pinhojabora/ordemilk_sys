from django.urls import path
from apps.configurador.views import(
        lista_configurador,
        cadastro_configurador, 
        editar_configuracao,
        detalhes_configurador,
        configurador_contencao,
        adicionar_contencao,
        adicionar_item_configurador,
        configurador_unidade_final,
        adicionar_unidade_final,
        configurador_sistema_limpeza,
        adicionar_sistema_limpeza,
        configurador_unidade_vacuo,
        adicionar_unidade_vacuo,
        ativa_gerenciamento,
        seleciona_gerenciamento,
        configurador_extrator,
        adicionar_extrator,
        configurador_conj_ordenha,
        adicionar_conj_ordenha,
        configurador_nobreak,
        adicionar_nobreak,
        converter_configuracao_orcamento
        
       ) 

urlpatterns = [
        path('index_configurador', lista_configurador, name='index_configurador'),
        path('cadastro_configurador', cadastro_configurador, name='cadastro_configurador'),
        path('editar_configurador/<int:configurador_id>/', editar_configuracao, name='editar_configurador'),
        path('detalhes_configurador/<int:configurador_id>/', detalhes_configurador, name='detalhes_configurador'),
        path('configurador_contencao/<int:configurador_id>/', configurador_contencao, name='configurador_contencao'),
        path('adicionar_contencao/', adicionar_contencao, name='adicionar_contencao'),
        path('configurador_unidade_final/<int:configurador_id>/', configurador_unidade_final, name='configurador_unidade_final'),
        path('adicionar_unidade_final/', adicionar_unidade_final, name='adicionar_unidade_final'),
        path('configurador_sistema_limpeza/<int:configurador_id>/', configurador_sistema_limpeza, name='configurador_sistema_limpeza'),
        path('adicionar_sistema_limpeza/', adicionar_sistema_limpeza, name='adicionar_sistema_limpeza'),
        path('configurador_unidade_vacuo/<int:configurador_id>/', configurador_unidade_vacuo, name='configurador_unidade_vacuo'),
        path('adicionar_unidade_vacuo/', adicionar_unidade_vacuo, name='adicionar_unidade_vacuo'),
        path('ativa_gerenciamento/<int:configurador_id>/', ativa_gerenciamento, name='ativa_gerenciamento'),
        path('seleciona_gerenciamento/<int:configurador_id>/', seleciona_gerenciamento, name='seleciona_gerenciamento'),
        path('configurador_extrator/<int:configurador_id>/', configurador_extrator, name='configurador_extrator'),
        path('adicionar_extrator/', adicionar_extrator, name='adicionar_extrator'),
        path('configurador_conj_ordenha/<int:configurador_id>/', configurador_conj_ordenha, name='configurador_conj_ordenha'),
        path('adicionar_conj_ordenha/', adicionar_conj_ordenha, name='adicionar_conj_ordenha'),
        path('configurador_nobreak/<int:configurador_id>/', configurador_nobreak, name='configurador_nobreak'),
        path('adicionar_nobreak/', adicionar_nobreak, name='adicionar_nobreak'),

        path('adicionar_item_configurador/', adicionar_item_configurador, name='adicionar_item_configurador'),
        path('converter_configuracao_para_orcamento/<int:configurador_id>/', converter_configuracao_orcamento, name='converter_configuracao_para_orcamento'),
]
