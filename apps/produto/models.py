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
    nome = models.TextField(max_length=100, null=False, blank=False)
    codigo = models.CharField(max_length=100, null=False, blank=False, default='')
    unidade = models.CharField(max_length=4, null=False, blank=False, default='')
    descricao = models.TextField(null=True, blank=True)
    peso = models.CharField(max_length=100, null=True, blank=True, default='')
    dimensoes = models.CharField(max_length=100, null=True, blank=True, default='')
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
    maximo_vacuo = models.IntegerField(null=True, blank=True, default=0)
    numero_conjuntos = models.IntegerField(null=True, blank=True, default=0)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']


class Producao1(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=2, blank=False, related_name='producao1s')
    codigo = models.CharField(max_length=100, null=False, blank=False, default='')
    nome = models.TextField(max_length=100, null=True, blank=True)
    quantidade = models.DecimalField(max_digits=30, decimal_places=5, null=True, blank=True, default=0)

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']

class Producao2(models.Model):
    producao1 = models.ForeignKey(Producao1, on_delete=models.CASCADE, null=False, blank=False, related_name='producao2s')
    codigo = models.CharField(max_length=100, null=True, blank=True, default='')
    nome = models.TextField(max_length=100, null=True, blank=True)
    quantidade = models.DecimalField(max_digits=30, decimal_places=5, null=True, blank=True, default=0)

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome'] 