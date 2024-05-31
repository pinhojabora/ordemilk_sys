from django.shortcuts import render, redirect, get_object_or_404

from apps.produto.models import Produto

from apps.carrinho.models import Carrinho
from apps.carrinho.forms import CarrinhoForms
from django.contrib import messages

from django.http import HttpResponse
from django.db.models import Q

def adicionar_carrinho(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        if produto_id:
            # Remove o separador de milhares do produto_id, se houver
            produto_id = produto_id.replace('.', '')

            try:
                produto = get_object_or_404(Produto, pk=produto_id)
                
                # Verifica se o produto já está no carrinho
                if Carrinho.objects.filter(produto=produto).exists():
                    messages.error(request, 'Este produto já está no carrinho.')
                else:
                    # Recupera o valor unitário com IPI do produto
                    valor_unitario_com_ipi = produto.preco_com_ipi
                    
                    # Adiciona o produto ao carrinho com o valor unitário com IPI
                    carrinho = Carrinho(produto=produto, quantidade=1, valor_unitario=valor_unitario_com_ipi, valor_total=valor_unitario_com_ipi)
                    carrinho.save()
                    messages.success(request, 'Produto adicionado ao carrinho com sucesso!')
            except ValueError:
                messages.error(request, 'ID do produto inválido.')
        else:
            messages.error(request, 'ID do produto não especificado.')
    
    return redirect('lista_carrinho')

def lista_carrinho(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    carrinhos = Carrinho.objects.all()
    return render(request, 'carrinho/index_carrinho.html', {"carrinhos": carrinhos})


def excluir_item_carrinho(request, carrinho_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    # Remove o separador de milhares do carrinho_id, se houver
    carrinho_id = carrinho_id.replace('.', '')

    try:
        carrinho_id = int(carrinho_id)  # Converte o carrinho_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do carrinho inválido.')
        return redirect('lista_carrinho')

    carrinho = get_object_or_404(Carrinho, pk=carrinho_id)
    carrinho.delete()
    messages.success(request, 'Item removido do carrinho com sucesso!')
    return redirect('lista_carrinho')


def editar_carrinho(request, carrinho_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    # Remove o separador de milhares do carrinho_id, se houver
    carrinho_id = carrinho_id.replace('.', '')

    try:
        carrinho_id = int(carrinho_id)  # Converte o carrinho_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do carrinho inválido.')
        return redirect('lista_carrinho')

    carrinho = get_object_or_404(Carrinho, pk=carrinho_id)
    form = CarrinhoForms(instance=carrinho)

    if request.method == 'POST':
        form = CarrinhoForms(request.POST, request.FILES, instance=carrinho)
        if form.is_valid():
            form.save()
            
            # Atualizar o valor total do item do carrinho
            carrinho.quantidade = form.cleaned_data['quantidade']
            carrinho.valor_unitario = form.cleaned_data['valor_unitario']
            carrinho.valor_total = carrinho.quantidade * carrinho.valor_unitario
            carrinho.save()
            
            messages.success(request, 'Carrinho editado com sucesso')
            return redirect('lista_carrinho')

    return render(request, 'carrinho/editar_carrinho.html', {'form': form, 'carrinho_id': carrinho_id})



def limpar_carrinho(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    carrinho_items = Carrinho.objects.all()
    
    # Lógica para excluir itens do carrinho após a importação
    carrinho_items.delete()

    return redirect('lista_carrinho')