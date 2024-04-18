from django.urls import path
from apps.dashboard.views import dashboard, dashboard_geral, dashboard_vendedor, dashboard_gerente, dashboard_todos_usuarios

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/geral/', dashboard_geral, name='dashboard_geral'),
    path('dashboard/vendedor/', dashboard_vendedor, name='dashboard_vendedor'),
    path('dashboard/gerente/', dashboard_gerente, name='dashboard_gerente'),
    path('dashboard/todos/', dashboard_todos_usuarios, name='dashboard_todos_usuarios'),
]