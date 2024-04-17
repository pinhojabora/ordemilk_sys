from django.db import models
from django.contrib.auth.models import User

class Estatistica_user(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    configuracao = models.IntegerField(null=True, blank=True, default=0)
    orcamento = models.IntegerField(null=True, blank=True, default=0)
    pedido = models.IntegerField(null=True, blank=True, default=0)
    efetivacao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
            return self.user.username

class Estatistica_geral(models.Model):
    configuracao = models.IntegerField(null=True, blank=True, default=0)
    orcamento = models.IntegerField(null=True, blank=True, default=0)
    pedido = models.IntegerField(null=True, blank=True, default=0)
    efetivacao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    