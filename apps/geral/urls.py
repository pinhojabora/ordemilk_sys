from django.urls import path
from apps.geral.views import index

urlpatterns = [
        path('', index, name='index'),
        
]
