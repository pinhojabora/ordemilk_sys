from django.shortcuts import render, redirect, get_object_or_404

from apps.orcamento.forms import OrcamentoForms, ItemOrcamentoInserirForm, ItemOrcamentoEditarForm, AdicionarParcelaForm

from django.contrib import messages
from apps.pedido.views import lista_pedido
from apps.orcamento.models import Orcamento, Item_orcamento, Parcela_orcamento
from apps.pedido.models import Pedido, Item_pedido
from apps.produto.models import Produto
from apps.carrinho.models import Carrinho
from django.http import HttpResponse
from django.db.models import Sum
from decimal import Decimal
from django.db.models import Q
from datetime import datetime


def lista_orcamento(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        orcamentos = Orcamento.objects.all()
        return render(request, 'orcamento/index_orcamento.html',{"orcamentos":orcamentos})

def cadastro_orcamento(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = OrcamentoForms(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Orçamento cadastrado com sucesso!')
            return redirect('index_orcamento')
        else:
            messages.error(request, 'Erro ao cadastrar o orçamento. Por favor, verifique os dados informados.')
    else:
        form = OrcamentoForms()
    return render(request, 'orcamento/cadastro_orcamento.html', {'form': form})

def detalhes_orcamento(request, orcamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    orcamento_detalhado = Orcamento.objects.get(pk=orcamento_id)
    itens_orcamento = Item_orcamento.objects.filter(orcamento=orcamento_detalhado)
    return render(request, 'orcamento/detalhes_orcamento.html', {'orcamento': orcamento_detalhado, 'itens_orcamento': itens_orcamento})


def editar_orcamento(request, orcamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    orcamento = Orcamento.objects.get(id=orcamento_id)
    form = OrcamentoForms(instance=orcamento)

    if request.method == 'POST':
        form = OrcamentoForms(request.POST, request.FILES, instance=orcamento)
        if form.is_valid():
            print(request.POST)
            form.save()
            messages.success(request, 'Orcamento editado com sucesso')
            return redirect('detalhes_orcamento',orcamento_id=orcamento_id)

    return render(request, 'orcamento/editar_orcamento.html', {'form': form, 'orcamento_id': orcamento_id})

def excluir_orcamento(request, orcamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    orcamento = get_object_or_404(Orcamento, pk=orcamento_id)
    
    if request.method == 'POST':
        # Verifica se o usuário confirmou a exclusão do pedido
        if 'confirmacao' in request.POST:
            orcamento.delete()
            messages.success(request, 'Orçamento excluído com sucesso!')
            return redirect(lista_orcamento)  
        else:
            messages.error(request, 'Você não confirmou a exclusão.')
            return redirect(lista_orcamento)
        
    return render(request, 'orcamento/excluir_orcamento.html', {'orcamento': orcamento})

def cadastro_item_orcamento(request, orcamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    orcamento = get_object_or_404(Orcamento, pk=orcamento_id)
    
    if request.method == 'POST':
        form = ItemOrcamentoInserirForm(request.POST)
        if form.is_valid():
            item_orcamento = form.save(commit=False)
            item_orcamento.orcamento = orcamento
            
            # Importar e salvar o preço do produto
            produto_id = form.cleaned_data['produto'].id
            produto = Produto.objects.get(pk=produto_id)
            item_orcamento.valor_unitario = produto.preco_com_ipi
            item_orcamento.valor_total = item_orcamento.quantidade * item_orcamento.valor_unitario
            
            item_orcamento.save()
            
            # Atualizar o valor_total do orçamento
            orcamento.valor_total += item_orcamento.valor_total
            orcamento.save()
            
            messages.success(request, 'Item do orçamento cadastrado com sucesso!')
            return redirect('detalhes_orcamento', orcamento_id=orcamento_id)
    else:
        form = ItemOrcamentoInserirForm()
    
    return render(request, 'orcamento/cadastro_item_orcamento.html', {'form': form, 'orcamento': orcamento})

def editar_item_orcamento(request, item_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    item = get_object_or_404(Item_orcamento, pk=item_id)
    
    if request.method == 'POST':
        form = ItemOrcamentoEditarForm(request.POST, instance=item)
        if form.is_valid():
            acrescimo = form.cleaned_data['acrescimo']
            desconto = form.cleaned_data['desconto']
            item.quantidade = form.cleaned_data['quantidade']
            item.valor_unitario = form.cleaned_data['valor_unitario']
            item.valor_total = item.quantidade * item.valor_unitario

            if acrescimo:
                item.valor_total += item.valor_total * (acrescimo / 100)
                item.valor_unitario = item.valor_total / item.quantidade
            elif desconto:
                item.valor_total -= item.valor_total * (desconto / 100)
                item.valor_unitario = item.valor_total / item.quantidade
            
            item.save()
            
            # Recalcular o valor total do orçamento após editar o item
            orcamento = item.orcamento
            itens_orcamento = Item_orcamento.objects.filter(orcamento=orcamento)
            total_orcamento = sum(item.valor_total for item in itens_orcamento)
            orcamento.valor_total = total_orcamento
            orcamento.save()

            messages.success(request, 'Item do orçamento atualizado com sucesso!')
            return redirect('detalhes_orcamento', orcamento_id=item.orcamento.id)
    else:
        form = ItemOrcamentoEditarForm(instance=item)
        # Calcular valor unitário após acréscimo/desconto e passar para o formulário
        if item.valor_total and item.quantidade:
            form.fields['valor_unitario'].initial = item.valor_total / item.quantidade
    
    return render(request, 'orcamento/editar_item_orcamento.html', {'form': form, 'item': item})

def excluir_item_orcamento(request, item_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    item = get_object_or_404(Item_orcamento, pk=item_id)
    
    if request.method == 'POST':
        orcamento = item.orcamento
        item.delete()
        
        # Recalcular o valor total do orçamento após excluir o item
        total_orcamento = Item_orcamento.objects.filter(orcamento=orcamento).aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        orcamento.valor_total = total_orcamento
        orcamento.save()
        
        return redirect('detalhes_orcamento', orcamento_id=orcamento.id)
    
    return render(request, 'orcamento/excluir_item_orcamento.html', {'item': item})


def editar_entrada_orcamento(request, orcamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    # Obter o objeto Orcamento existente ou retornar 404 se não encontrado
    orcamento = get_object_or_404(Orcamento, pk=orcamento_id)

    if request.method == 'POST':
        # Obter o valor de entrada do formulário e converter para Decimal
        entrada_str = request.POST.get('entrada')
        entrada_decimal = Decimal(entrada_str)

        # Atualizar o valor de entrada do orçamento
        orcamento.entrada = entrada_decimal
        # Calcular o saldo subtraindo a entrada do valor total
        orcamento.saldo = orcamento.valor_total - orcamento.entrada
        # Salvar as alterações no orçamento
        orcamento.save()

        # Redirecionar para a página de detalhes do orçamento ou para onde desejar
        return redirect('detalhes_orcamento', orcamento_id=orcamento.id)

    # Se não for um POST, exibir o formulário de edição do orçamento
    return render(request, 'orcamento/editar_entrada_orcamento.html', {'orcamento': orcamento})


def adicionar_parcela(request, orcamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    orcamento = Orcamento.objects.get(pk=orcamento_id)
    
    if request.method == 'POST':
        form = AdicionarParcelaForm(request.POST)
        if form.is_valid():
            parcela = form.save(commit=False)
            parcela.orcamento = orcamento
            parcela.save()
            return redirect('detalhes_orcamento', orcamento_id=orcamento_id)
    else:
        form = AdicionarParcelaForm()
    
    return render(request, 'orcamento/adicionar_parcela.html', {'form': form,'orcamento': orcamento})

def editar_parcela(request, parcela_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    # Obtenha a parcela existente a ser editada
    parcela = get_object_or_404(Parcela_orcamento, pk=parcela_id)

    if request.method == 'POST':
        # Crie um formulário de parcela com os dados atualizados
        form = AdicionarParcelaForm(request.POST, instance=parcela)
        if form.is_valid():
            form.save()
            return redirect('detalhes_orcamento', orcamento_id=parcela.orcamento.id)
    else:
        # Preencha o formulário com os dados existentes da parcela
        form = AdicionarParcelaForm(instance=parcela)

    return render(request, 'orcamento/editar_parcela.html', {'form': form, 'parcela': parcela})

def excluir_parcela(request, parcela_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    # Obtenha a parcela existente a ser excluída
    parcela = get_object_or_404(Parcela_orcamento, pk=parcela_id)

    if request.method == 'POST':
        # Exclua a parcela
        parcela.delete()
        return redirect('detalhes_orcamento', orcamento_id=parcela.orcamento.id)

    return render(request, 'orcamento/excluir_parcela.html', {'parcela': parcela})


def converter_orcamento_pedido(request, orcamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    try:
        orcamento = Orcamento.objects.get(pk=orcamento_id)
        
        # Criar o pedido com base nos dados do orçamento
        novo_pedido = Pedido.objects.create(
            data_pedido=orcamento.data_orcamento,
            nome_cliente=orcamento.nome_cliente,
            endereco_cliente=orcamento.endereco_cliente,
            cidade=orcamento.cidade,
            estado=orcamento.estado,
            cep=orcamento.cep,
            cnpj_cpf=orcamento.cnpj_cpf,
            insc_estadual=orcamento.insc_estadual,
            fone=orcamento.fone,
            email=orcamento.email,
            forma_pagamento=orcamento.forma_pagamento,
            pagamento=orcamento.pagamento,
            valor_total=orcamento.valor_total,
            entrada=orcamento.entrada,
            saldo=orcamento.saldo,
            parcelas=orcamento.parcelas,
            observacao=orcamento.observacao,
            usuario=orcamento.usuario,
        )
        
        # Copiar itens do orçamento para o pedido
        for item_orcamento in orcamento.item_orcamento_set.all():
            Item_pedido.objects.create(
                pedido=novo_pedido,
                produto=item_orcamento.produto,
                quantidade=item_orcamento.quantidade,
                valor_unitario=item_orcamento.valor_unitario,
                valor_total=item_orcamento.valor_total,
            )
        
        # Exibir mensagem de sucesso
        messages.success(request, 'Orçamento convertido em pedido com sucesso!')
        return redirect(lista_pedido)
       
        
    except Exception as e:
        # Exibir mensagem de erro
        messages.error(request, f'Erro ao converter orçamento em pedido: {e}')
    
    # Redirecionar de volta para a página de index de orçamentos
    return redirect('index_orcamento')

def importar_produtos(request, orcamento_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    carrinho_items = Carrinho.objects.all()
    
    if not carrinho_items.exists():
        messages.error(request, 'O carrinho está vazio. Não há itens para importar.')
        return redirect('carrinho_vazio')  # Redireciona para a página de carrinho vazio

    orcamento = get_object_or_404(Orcamento, pk=orcamento_id)

    # Lógica para importar produtos do carrinho para itens do orçamento
    for carrinho_item in carrinho_items:
        orcamento.item_orcamento_set.create(
            produto=carrinho_item.produto,
            quantidade=carrinho_item.quantidade,
            valor_unitario=carrinho_item.valor_unitario,
            valor_total=carrinho_item.valor_total,
        )

    # Atualizar o valor total do orçamento
    orcamento.valor_total = sum(item.valor_total for item in orcamento.item_orcamento_set.all())
    orcamento.save()

    # Lógica para excluir itens do carrinho após a importação
    carrinho_items.delete()

    return redirect('detalhes_orcamento', orcamento_id=orcamento_id)


def buscar_orcamento(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    orcamentos = None
    termo_busca = None

    if "buscar_orcamento" in request.GET:
        termo_busca = request.GET['buscar_orcamento']
        # Tenta converter o termo de busca para data no formato correto (AAAA-MM-DD)
        try:
            data_busca = datetime.strptime(termo_busca, '%d/%m/%Y').date()
            # Filtra os orçamentos por data do orçamento se a conversão for bem-sucedida
            orcamentos = Orcamento.objects.filter(data_orcamento=data_busca)
        except ValueError:
            # Se a conversão falhar, trata o termo de busca como nome do cliente
            orcamentos = Orcamento.objects.filter(nome_cliente__icontains=termo_busca)
            
    return render(request, 'orcamento/buscar_orcamento.html', {'orcamentos': orcamentos, 'termo_busca': termo_busca})

def carrinho_vazio(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        return render(request, 'carrinho/carrinho_vazio.html')