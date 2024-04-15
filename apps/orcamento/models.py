from django.db import models

from datetime import datetime, date

from apps.produto.models import Produto

from django.contrib.auth.models import User

class Orcamento(models.Model):
    OPCOES_FORPAGAMENTO = [
        ("A VISTA","A Vista"),
        ("FINANCIADO","Financiado"),
        ("ENTRADA + PARCELAS","Entrada + parcelas"),
    ]

    OPCOES_PAGAMENTO = [
        ("DINHEIRO","Dinheiro"),
        ("CHEQUE","Cheque"),
        ("DEPOSITO","Depósito"),
        ("BOLETO","Boleto"),
    ]

    data_orcamento = models.DateField(default=datetime.today, blank=False)
    nome_cliente = models.CharField(max_length=100, null=False, blank=False)
    endereco_cliente = models.CharField(max_length=100, null=False, blank=False)
    cidade = models.CharField(max_length=100, null=False, blank=False, default='')
    estado = models.CharField(max_length=2, null=False, blank=False, default='')
    cep = models.CharField(max_length=9, null=False, blank=False, default='')
    cnpj_cpf = models.CharField(max_length=18, null=False, blank=False, default='')
    insc_estadual = models.CharField(max_length=25, null=False, blank=False, default='')
    fone = models.CharField(max_length=25, null=False, blank=False, default='')
    email = models.CharField(max_length=100, null=False, blank=False, default='')
    forma_pagamento = models.CharField(max_length=100, choices=OPCOES_FORPAGAMENTO, default='')
    pagamento = models.CharField(max_length=100, choices=OPCOES_PAGAMENTO, default='')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    entrada = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    parcelas = models.CharField(max_length=100, null=False, blank=False, default=0)
    observacao = models.TextField(null=False, blank=False)
    usuario = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orcamento'
    )

    def __str__(self):
        return self.nome_cliente
    

class Item_orcamento(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, null=True, blank=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=False, related_name='orcamentos')
    quantidade = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Parcela_orcamento(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, null=True, blank=True)
    data_parcela = models.DateField(default=datetime.today, blank=False)
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
