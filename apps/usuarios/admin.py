from django.contrib import admin
from django.contrib.auth.models import User
from .models import Gerente, Vendedor

admin.site.register(Gerente)
admin.site.register(Vendedor)

