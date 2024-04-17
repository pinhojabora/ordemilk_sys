from django.urls import path
from apps.dashboard.views import dashboard, dashboard_geral

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/geral/', dashboard_geral, name='dashboard_geral'),
]