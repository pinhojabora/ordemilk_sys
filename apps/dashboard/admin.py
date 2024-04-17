from django.contrib import admin

from apps.dashboard.models import Estatistica_geral, Estatistica_user

admin.site.register(Estatistica_geral)
admin.site.register(Estatistica_user)