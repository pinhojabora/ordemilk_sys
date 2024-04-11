from django.db import models

class Tensao_energia(models.Model):
    tensao_energia_nome = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.tensao_energia_nome

class Modelo_sala(models.Model):
    modelo_sala_nome = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.modelo_sala_nome

class Modelo_equipamento(models.Model):
    modelo_equipamento_nome = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.modelo_equipamento_nome

class Tipo_linha(models.Model):
    tipo_linha_nome = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.tipo_linha_nome
    
class Tipo_contencao(models.Model):
    tipo_contencao_nome = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.tipo_contencao_nome

class Tipo_gerenciamento(models.Model):
    tipo_gerenciamento_nome = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.tipo_gerenciamento_nome