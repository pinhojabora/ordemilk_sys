from django.db import models

from datetime import datetime

from apps.ferramentas.models import Tensao_energia, Modelo_sala, Modelo_equipamento, Tipo_linha, Tipo_contencao, Tipo_gerenciamento

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    
        
    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']

class Subcategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']

             
class Produto(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    codigo = models.CharField(max_length=100, null=False, blank=False, default='')
    unidade = models.CharField(max_length=4, null=False, blank=False, default='')
    descricao = models.TextField(null=False, blank=False)
    peso = models.CharField(max_length=100, null=False, blank=False, default='')
    dimensoes = models.CharField(max_length=100, null=False, blank=False, default='')
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preco_com_ipi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, null=True, blank=True)
    tensao_energia = models.ForeignKey(Tensao_energia, on_delete=models.CASCADE, null=True, blank=True)
    modelo_sala = models.ForeignKey(Modelo_sala, on_delete=models.CASCADE, null=True, blank=True)
    modelo_equipamento = models.ForeignKey(Modelo_equipamento, on_delete=models.CASCADE, null=True, blank=True)
    tipo_linha = models.ForeignKey(Tipo_linha, on_delete=models.CASCADE, null=True, blank=True)
    tipo_contencao = models.ForeignKey(Tipo_contencao, on_delete=models.CASCADE, null=True, blank=True)
    sistema_limpeza = models.BooleanField(default=False)
    tipo_gerenciamento = models.ForeignKey(Tipo_gerenciamento, on_delete=models.CASCADE, null=True, blank=True)
    extracao = models.BooleanField(default=False)
    conj_ordenha = models.BooleanField(default=False)
    nobreak = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    

