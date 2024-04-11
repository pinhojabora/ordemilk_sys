from django.db import models

from datetime import datetime

from apps.produto.models import Produto

class Fotografia(models.Model):

    nome = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=150, null=False, blank=False)
    descricao = models.TextField(null=False, blank=False)
    foto = models.ImageField(upload_to="fotos", blank=True)
    data_fotografia = models.DateTimeField(default=datetime.now, blank=False)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=False, related_name='fotografias')

    def __str__(self):
        return self.nome
