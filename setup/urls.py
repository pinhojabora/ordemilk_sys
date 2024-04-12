from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
        path('controle-geral/', admin.site.urls),
        path('', include('apps.geral.urls')),
        path('', include('apps.usuarios.urls')),
        path('', include('apps.produto.urls')),
        path('', include('apps.galeria.urls')),
        path('', include('apps.orcamento.urls')),
        path('', include('apps.pedido.urls')),
        path('', include('apps.configurador.urls')),
        path('', include('apps.ferramentas.urls')),
        path('', include('apps.carrinho.urls')),
        
        
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

