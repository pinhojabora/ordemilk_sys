from django.contrib import admin
from apps.produto.models import Produto, Categoria, Subcategoria, Producao1, Producao2


class ListandoProducao1(admin.ModelAdmin):
    list_display = ("produto_id","codigo","nome", "quantidade")
    list_display_links = ("codigo","nome")
    list_per_page = 100
    list_filter = ("produto_id",)




class ListandoProduto(admin.ModelAdmin):
    list_display = ("codigo","descricao","unidade","peso","dimensoes","preco","preco_com_ipi")
    list_display_links = ("codigo","descricao")
    search_fields = ("codigo","descricao")
    list_filter = ("categoria","subcategoria",)
    list_per_page = 20

admin.site.register(Produto, ListandoProduto),
admin.site.register(Categoria),
admin.site.register(Subcategoria),
admin.site.register(Producao1, ListandoProducao1),
admin.site.register(Producao2),

