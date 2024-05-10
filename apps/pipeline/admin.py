from django.contrib import admin
from apps.pipeline.models import Fase_pipeline, Situacao_pipeline, Historico_pipeline, Itens_pipeline, Envolvido_pipeline, Atividade_pipeline, Pipeline

admin.site.register(Fase_pipeline)
admin.site.register(Situacao_pipeline)
admin.site.register(Historico_pipeline)
admin.site.register(Itens_pipeline)
admin.site.register(Envolvido_pipeline)
admin.site.register(Atividade_pipeline)
admin.site.register(Pipeline)