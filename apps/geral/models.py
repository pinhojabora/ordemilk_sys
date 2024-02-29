from django.db import models

from datetime import datetime

class conversa(models.Model):
    titulo = models.CharField(max_length=100, null=False, blank=False)
    mensagem = models.TextField(null=False, blank=False)
    data_mensagem = models.DateTimeField(default=datetime.now, blank=False)
    lida = models.BooleanField(default=False)
    autor = models.CharField(max_length=100, null=False, blank=False, default='')
    categoria = models.CharField(max_length=100, null=False, blank=False, default='')

def __str__(self):
    return self.nome
