from django.urls import path
from apps.produto.views import produto
 
urlpatterns = [
        path('produto', produto, name='produto')
]
