from django.urls import path
from apps.pipeline.views import(
    cadastro_prospecto,
    quadro_pipeline,
    detalhes_prospecto,
    editar_prospecto,
    adicionar_envolvido,
    excluir_envolvido,
    adicionar_item,
    editar_proposta,
    mover_pipeline,
    quadro_geral_pipeline,

) 

urlpatterns = [
        path('index_pipeline', quadro_pipeline, name='index_pipeline'),
        path('index_geral_pipeline', quadro_geral_pipeline, name='index_geral_pipeline'),
        path('cadastro_prospecto', cadastro_prospecto, name='cadastro_prospecto'),
        path('detalhes_prospecto/<int:pipeline_id>/', detalhes_prospecto, name='detalhes_prospecto'),
        path('editar_prospecto/<int:pipeline_id>/',editar_prospecto, name='editar_prospecto'),
        path('adicionar_envolvido/<int:pipeline_id>/', adicionar_envolvido, name='adicionar_envolvido'),
        path('excluir_envolvido/<int:envolvido_pipeline_id>/', excluir_envolvido, name='excluir_envolvido'),
        path('adicionar_item/<int:pipeline_id>/', adicionar_item, name='adicionar_item'),
        path('editar_proposta/<int:pipeline_id>/',editar_proposta, name='editar_proposta'),
        path('mover_pipeline/<int:pipeline_id>/',mover_pipeline, name='mover_pipeline'),
]