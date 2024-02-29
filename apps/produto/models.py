from django.db import models

from datetime import datetime

class produto(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    codigo = models.CharField(max_length=100, null=False, blank=False, default='')
    unidade = models.CharField(max_length=4, null=False, blank=False, default='')
    descricao = models.TextField(null=False, blank=False)
    peso = models.CharField(max_length=100, null=False, blank=False, default='')
    dimensoes = models.CharField(max_length=100, null=False, blank=False, default='')
    categoria = models.CharField(max_length=100, null=False, blank=False, default='')
    
def __str__(self):
    return self.nome