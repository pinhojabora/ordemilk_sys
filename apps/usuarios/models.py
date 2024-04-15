from django.db import models
from django.contrib.auth.models import User

    
class Gerente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
class Vendedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gerente = models.ForeignKey(Gerente, on_delete=models.CASCADE, related_name='vendedor')
    def __str__(self):
        return self.user.username

    