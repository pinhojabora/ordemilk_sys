from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.utils import timezone
from apps.produto.models import Produto

class Fase_pipeline(models.Model):
    nome_fase = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.nome_fase
    
class Situacao_pipeline(models.Model):
    nome_situacao = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.nome_situacao

class Pipeline(models.Model):
    data_inclusao = models.DateField(default=timezone.now, blank=False)
    titulo = models.CharField(max_length=100, null=False, blank=False)
    cliente = models.CharField(max_length=100, null=False, blank=False)
    pessoa_contato = models.CharField(max_length=100, null=True, blank=True)
    telefone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=False, blank=False)
    estado = models.CharField(max_length=100, null=False, blank=False)
    setor_atividade = models.CharField(max_length=100, null=False, blank=False)
    fonte_lead = models.CharField(max_length=100, null=False, blank=False)
    detalhes_oportunidade = models.TextField(null=False, blank=False)
    demo_tecnica = models.BooleanField(default=False)
    produto_customizado = models.TextField(null=True, blank=True)
    detalhes_proposta = models.TextField(null=True, blank=True)
    total_proposta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    desconto_proposta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    acrescimo_proposta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    final_proposta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    validade_proposta = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pipeline')
    fase = models.ForeignKey(Fase_pipeline,on_delete=models.SET_DEFAULT, null=True, blank=True, related_name='pipeline', default=1)
    situacao = models.ForeignKey(Situacao_pipeline,on_delete=models.SET_NULL, null=True, blank=True, related_name='pipeline')
    
    def __str__(self):
        return self.titulo
    

    

class Historico_pipeline(models.Model):
    fase = models.ForeignKey(Fase_pipeline, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='historico_pipeline')
    data_fase = models.DateField(default=timezone.now, blank=False)
    usuario = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True, related_name='historico_pipeline')


class Itens_pipeline(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=False, blank=False, related_name='itens_pipeline')
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='itens_pipeline')



class Envolvido_pipeline(models.Model):
     envolvido = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='envolvido_pipeline')


class Atividade_pipeline(models.Model):
     data_atividade = models.DateField(default=timezone.now, blank=False)
     atividade = models.CharField(max_length=300, null=False, blank=False)
     pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=False, blank=False, related_name='atividade_pipeline')
     usuario = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True, related_name='atividade_pipeline')

     def __str__(self):
        return self.atividade