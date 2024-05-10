from django.urls import path
from apps.pipeline.views import cadastro_prospecto, quadro_pipeline, detalhes_prospecto

urlpatterns = [
        path('index_pipeline', quadro_pipeline, name='index_pipeline'),
        path('cadastro_prospecto', cadastro_prospecto, name='cadastro_prospecto'),
        path('detalhes_prospecto/<int:pipeline_id>/', detalhes_prospecto, name='detalhes_prospecto'),
]