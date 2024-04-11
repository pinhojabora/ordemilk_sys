from django.shortcuts import render, redirect, get_object_or_404

from apps.pedido.forms import PedidoForms

from django.contrib import messages

from apps.pedido.models import Pedido, Item_pedido
from apps.carrinho.models import Carrinho
from datetime import datetime
from django.http import HttpResponse



def lista_pedido(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        pedidos = Pedido.objects.all()
        return render(request, 'pedido/index_pedido.html',{"pedidos":pedidos})

def cadastro_pedido(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = PedidoForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido cadastrado com sucesso!')
            return redirect('index_pedido')
        else:
            messages.error(request, 'Erro ao cadastrar o pedido. Por favor, verifique os dados informados.')
    else:
        form = PedidoForms()
    return render(request, 'pedido/cadastro_pedido.html', {'form': form})


def detalhes_pedido(request, pedido_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    pedido_detalhado = Pedido.objects.get(pk=pedido_id)
    itens_pedido = Item_pedido.objects.filter(pedido=pedido_detalhado)
    return render(request, 'pedido/detalhes_pedido.html', {'pedido': pedido_detalhado, 'itens_pedido': itens_pedido})


def editar_pedido(request, pedido_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    pedido = Pedido.objects.get(id=pedido_id)
    form = PedidoForms(instance=pedido)

    if request.method == 'POST':
        form = PedidoForms(request.POST, request.FILES, instance=pedido)
        if form.is_valid():
            print(request.POST)
            form.save()
            messages.success(request, 'Pedido editado com sucesso')
            return redirect('index_pedido')

    return render(request, 'pedido/editar_pedido.html', {'form': form, 'pedido_id': pedido_id})


def excluir_pedido(request, pedido_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    
    if request.method == 'POST':
        # Verifica se o usuário confirmou a exclusão do pedido
        if 'confirmacao' in request.POST:
            pedido.delete()
            messages.success(request, 'Pedido excluído com sucesso!')
            return redirect(lista_pedido)  # Redireciona para a página de index de pedidos ou outra página desejada após a exclusão
        else:
            messages.error(request, 'Você não confirmou a exclusão.')
            return redirect('detalhes_pedido', pedido_id=pedido_id)  # Redireciona de volta para a página de detalhes do pedido
        
    return render(request, 'pedido/excluir_pedido.html', {'pedido': pedido})

def importar_produtos_pedido(request, pedido_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    carrinho_items = Carrinho.objects.all()

    if not carrinho_items.exists():
        messages.error(request, 'O carrinho está vazio. Não há itens para importar.')
        return redirect('carrinho_vazio')  # Redireciona para a página de carrinho vazio

    pedido = get_object_or_404(Pedido, pk=pedido_id)

    # Lógica para importar produtos do carrinho para itens do pedido
    for carrinho_item in carrinho_items:
        pedido.item_pedido_set.create(
            produto=carrinho_item.produto,
            quantidade=carrinho_item.quantidade,
            valor_unitario=carrinho_item.valor_unitario,
            valor_total=carrinho_item.valor_total,
        )
    
    # Atualizar o valor total do pedido
    pedido.valor_total = sum(item.valor_total for item in pedido.item_pedido_set.all())
    pedido.save()

    # Lógica para excluir itens do carrinho após a importação
    carrinho_items.delete()

    return redirect('detalhes_pedido', pedido_id=pedido_id)


def buscar_pedido(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    pedidos = None
    termo_busca = None

    if "buscar_pedido" in request.GET:
        termo_busca = request.GET['buscar_pedido']
        # Tenta converter o termo de busca para data no formato correto (AAAA-MM-DD)
        try:
            data_busca = datetime.strptime(termo_busca, '%d/%m/%Y').date()
            # Filtra os orçamentos por data do orçamento se a conversão for bem-sucedida
            pedidos = Pedido.objects.filter(data_pedido=data_busca)
        except ValueError:
            # Se a conversão falhar, trata o termo de busca como nome do cliente
            pedidos = Pedido.objects.filter(nome_cliente__icontains=termo_busca)
            
    return render(request, 'pedido/buscar_pedido.html', {'pedidos': pedidos, 'termo_busca': termo_busca})