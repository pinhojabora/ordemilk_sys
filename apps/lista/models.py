from django.db import models

from datetime import datetime

class Lista(models.Model):
    nome_lista = models.CharField(max_length=100, null=False, blank=False)
    periodo = models.CharField(max_length=100, null=False, blank=False, default='')
    vigencia = models.CharField(max_length=100, null=False, blank=False, default='')
    data_lista = models.DateTimeField(default=datetime.now, blank=False)
    observacao = models.TextField(null=False, blank=False)
    ativa = models.BooleanField(default=False)
        
    def __str__(self):
        return self.nome_lista
    
