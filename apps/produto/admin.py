from django.contrib import admin
from apps.produto.models import Produto, Categoria, Subcategoria



class ListandoProduto(admin.ModelAdmin):
    list_display = ("codigo","descricao","unidade","peso","dimensoes","preco","preco_com_ipi")
    list_display_links = ("codigo","descricao")
    search_fields = ("codigo","descricao")
    list_filter = ("categoria","subcategoria",)
    list_per_page = 20

admin.site.register(Produto, ListandoProduto),
admin.site.register(Categoria),
admin.site.register(Subcategoria),