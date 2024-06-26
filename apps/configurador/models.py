from django.db import models

from datetime import datetime, date

from apps.ferramentas.models import Tensao_energia, Modelo_sala, Modelo_equipamento, Tipo_linha, Tipo_contencao, Tipo_gerenciamento
from apps.produto.models import Produto
from django.contrib.auth.models import User

class Configurador(models.Model):
    data_configuracao = models.DateField(default=datetime.today, blank=False)
    nome_cliente = models.CharField(max_length=100, null=False, blank=False)
    nome_fazenda = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=False, blank=False, default='')
    estado = models.CharField(max_length=2, null=False, blank=False, default='')
    fone = models.CharField(max_length=25, null=False, blank=False, default='')
    tensao_energia = models.ForeignKey(Tensao_energia, on_delete=models.CASCADE, null=True, blank=True) 
    modelo_sala = models.ForeignKey(Modelo_sala, on_delete=models.CASCADE, null=True, blank=True)
    modelo_equipamento = models.ForeignKey(Modelo_equipamento, on_delete=models.CASCADE, null=True, blank=True)
    tipo_linha = models.ForeignKey(Tipo_linha, on_delete=models.CASCADE, null=True, blank=True)
    tipo_contencao = models.ForeignKey(Tipo_contencao, on_delete=models.CASCADE, null=True, blank=True)
    gerenciamento = models.BooleanField(default=False)
    tipo_gerenciamento = models.ForeignKey(Tipo_gerenciamento, on_delete=models.CASCADE, null=True, blank=True)
    quant_gerenciamento = models.CharField(max_length=100, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0) 
    vacuo_recomendado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    altitude = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True, default=0)
    numero_conjuntos = models.IntegerField(null=True, blank=True, default=0)
    fator_calculo_modelo = models.IntegerField(null=True, blank=True, default=0)
    usuario = models.ForeignKey(
            to=User,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='configurador'
        )
    
    def save(self, *args, **kwargs):
        if self.modelo_equipamento:
            self.fator_calculo_modelo = self.modelo_equipamento.fator_calculo
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_cliente
 
class Item_configurador(models.Model):
    configurador = models.ForeignKey(Configurador, on_delete=models.CASCADE, null=True, blank=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=False, related_name='configurador')
    quantidade = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    

