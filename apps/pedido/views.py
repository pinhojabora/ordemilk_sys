from django.shortcuts import render, redirect, get_object_or_404
from apps.pedido.forms import PedidoForms, AdicionarParcelaPedidoForm, ItemPedidoInserirForm, ItemPedidoEditarForm
from django.contrib import messages
from apps.dashboard.models import Estatistica_user, Estatistica_geral
from apps.pedido.models import Pedido, Item_pedido, Parcela_pedido
from apps.carrinho.models import Carrinho
from datetime import datetime
from django.http import HttpResponse
from apps.produto.models import Producao1, Producao2, Produto
from decimal import Decimal
from django.db.models import Sum
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from io import BytesIO

def lista_pedido(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        pedidos = Pedido.objects.all()
        return render(request, 'pedido/index_pedido.html',{"pedidos":pedidos})

def calcular_efetivacao(orcamento, pedido):
    orcamento_decimal = Decimal(orcamento)
    pedido_decimal = Decimal(pedido)
    
    if orcamento_decimal == Decimal(0):
        return Decimal(0)
    
    return ((pedido_decimal - orcamento_decimal) / orcamento_decimal) * Decimal(100)

def cadastro_pedido(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if request.method == 'POST':
        form = PedidoForms(request.POST)
        if form.is_valid():
            pedido_instance = form.save(commit=False)
            pedido_instance.usuario = request.user  # Definindo o usuário do pedido
            pedido_instance.save()

            # Atualiza as estatísticas do usuário
            estatistica_user = Estatistica_user.objects.get_or_create(user=request.user)[0]
            estatistica_user.pedido += 1
            estatistica_user.efetivacao = calcular_efetivacao(estatistica_user.orcamento, estatistica_user.pedido)
            estatistica_user.save()

            # Atualiza as estatísticas gerais
            estatistica_geral = Estatistica_geral.objects.first()
            estatistica_geral.pedido += 1
            estatistica_geral.efetivacao = calcular_efetivacao(estatistica_geral.orcamento, estatistica_geral.pedido)
            estatistica_geral.save()

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
            # Atualiza as estatísticas do usuário
            estatistica_user = Estatistica_user.objects.get_or_create(user=request.user)[0]
            estatistica_user.pedido -= 1
            estatistica_user.efetivacao = calcular_efetivacao(estatistica_user.orcamento, estatistica_user.pedido)
            estatistica_user.save()

            # Atualiza as estatísticas gerais
            estatistica_geral = Estatistica_geral.objects.first()
            estatistica_geral.pedido -= 1
            estatistica_geral.efetivacao = calcular_efetivacao(estatistica_geral.orcamento, estatistica_geral.pedido)
            estatistica_geral.save()

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


def romaneio_pedido(request, pedido_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    pedido_detalhado = get_object_or_404(Pedido, pk=pedido_id)
    
    itens_pedido = Item_pedido.objects.filter(pedido=pedido_detalhado)
    
    producao1s = []
    for item in itens_pedido:
        producao1s.extend(Producao1.objects.filter(produto=item.produto))

    producao2s = []
    for producao1 in producao1s:
        producao2s.extend(Producao2.objects.filter(producao1=producao1))

    return render(request, 'pedido/romaneio_pedido.html', {
        'pedido': pedido_detalhado,
        'itens_pedido': itens_pedido,
        'producao1s': producao1s,
        'producao2s': producao2s,
    })


def imprimir_romaneio_pdf(request, pedido_id):
    pedido_detalhado = get_object_or_404(Pedido, pk=pedido_id)
    itens_pedido = Item_pedido.objects.filter(pedido=pedido_detalhado)
    producao1s = Producao1.objects.filter(produto__in=[item.produto for item in itens_pedido])
    producao2s = Producao2.objects.filter(producao1__in=producao1s)

    context = {
        'pedido_detalhado': pedido_detalhado,
        'itens_pedido': itens_pedido,
        'producao1s': producao1s,
        'producao2s': producao2s,
    }

    # Renderizar o template HTML em uma string
    html_string = render_to_string('pedido/romaneio_template.html', context)

    # Criar um arquivo BytesIO para armazenar o PDF
    pdf_file = BytesIO()

    # Criar o PDF usando xhtml2pdf
    pisa.CreatePDF(BytesIO(html_string.encode("UTF-8")), dest=pdf_file)

    # Configurar o cursor do BytesIO para o início antes de enviar o conteúdo
    pdf_file.seek(0)

    # Configurar a resposta HTTP com o conteúdo PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="romaneio_pedido.pdf"'

    return response


def imprimir_pedido_pdf(request, pedido_id):
    pedido_detalhado = get_object_or_404(Pedido, pk=pedido_id)
    itens_pedido = Item_pedido.objects.filter(pedido=pedido_detalhado)
    parcelas_pedido = Parcela_pedido.objects.filter(pedido=pedido_detalhado)

    context = {
        'pedido_detalhado': pedido_detalhado,
        'itens_pedido': itens_pedido,
        'parcelas_pedido': parcelas_pedido,
    }

    # Renderizar o template HTML em uma string
    html_string = render_to_string('pedido/impressao_pedido.html', context)

    # Criar um arquivo BytesIO para armazenar o PDF
    pdf_file = BytesIO()

    # Criar o PDF usando xhtml2pdf
    pisa.CreatePDF(BytesIO(html_string.encode("UTF-8")), dest=pdf_file)

    # Configurar o cursor do BytesIO para o início antes de enviar o conteúdo
    pdf_file.seek(0)

    # Configurar a resposta HTTP com o conteúdo PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="impressao_pedido.pdf"'

    return response


def adicionar_parcela_pedido(request, pedido_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    pedido = get_object_or_404(Pedido, pk=pedido_id)

    if request.method == 'POST':
        form = AdicionarParcelaPedidoForm(request.POST)
        if form.is_valid():
            parcela = form.save(commit=False)
            parcela.pedido = pedido

            # Calculate valor_parcela based on total value divided by number of parcelas
            valor_total = pedido.saldo
            quantia_parcelas = int(pedido.parcelas)
            if quantia_parcelas > 0:
                parcela.valor_parcela = valor_total / quantia_parcelas
            else:
                messages.error(request, 'A quantia de parcelas deve ser maior que zero.')
                return render(request, 'pedido/adicionar_parcela.html', {'form': form, 'pedido': pedido})

            # Debugging prints
            print(f'Valor total: {valor_total}, Quantia parcelas: {quantia_parcelas}, Valor parcela: {parcela.valor_parcela}')

            parcela.save()
            messages.success(request, 'Parcela adicionada com sucesso!')
            return redirect('detalhes_pedido', pedido_id=pedido_id)
        else:
            messages.error(request, 'Erro ao adicionar parcela. Verifique os dados informados.')
    else:
        form = AdicionarParcelaPedidoForm()

    return render(request, 'pedido/adicionar_parcela.html', {'form': form, 'pedido': pedido})

def editar_parcela_pedido(request, parcela_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    # Obtenha a parcela existente a ser editada
    parcela = get_object_or_404(Parcela_pedido, pk=parcela_id)

    if request.method == 'POST':
        # Crie um formulário de parcela com os dados atualizados
        form = AdicionarParcelaPedidoForm(request.POST, instance=parcela)
        if form.is_valid():
            form.save()
            return redirect('detalhes_pedido', pedido_id=parcela.pedido.id)
    else:
        # Preencha o formulário com os dados existentes da parcela
        form = AdicionarParcelaPedidoForm(instance=parcela)

    return render(request, 'pedido/editar_parcela.html', {'form': form, 'parcela': parcela})

def excluir_parcela_pedido(request, parcela_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    # Obtenha a parcela existente a ser excluída
    parcela = get_object_or_404(Parcela_pedido, pk=parcela_id)

    if request.method == 'POST':
        # Exclua a parcela
        parcela.delete()
        return redirect('detalhes_pedido', pedido_id=parcela.pedido.id)

    return render(request, 'pedido/excluir_parcela.html', {'parcela': parcela})


def cadastro_item_pedido(request, pedido_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    
    if request.method == 'POST':
        form = ItemPedidoInserirForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            item_pedido.pedido = pedido
            
            # Importar e salvar o preço do produto
            produto_id = form.cleaned_data['produto'].id
            produto = Produto.objects.get(pk=produto_id)
            item_pedido.valor_unitario = produto.preco_com_ipi
            item_pedido.valor_total = item_pedido.quantidade * item_pedido.valor_unitario
            
            item_pedido.save()
            
            # Atualizar o valor_total do orçamento
            pedido.valor_total += item_pedido.valor_total
            pedido.save()
            
            messages.success(request, 'Item do pedido cadastrado com sucesso!')
            return redirect('detalhes_pedido', pedido_id=pedido_id)
    else:
        form = ItemPedidoInserirForm()
    
    return render(request, 'pedido/cadastro_item_pedido.html', {'form': form, 'pedido': pedido})

def editar_item_pedido(request, item_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    item = get_object_or_404(Item_pedido, pk=item_id)
    
    if request.method == 'POST':
        form = ItemPedidoEditarForm(request.POST, instance=item)
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
            pedido = item.pedido
            itens_pedido = Item_pedido.objects.filter(pedido=pedido)
            total_pedido = sum(item.valor_total for item in itens_pedido)
            pedido.valor_total = total_pedido
            pedido.save()

            messages.success(request, 'Item do pedido atualizado com sucesso!')
            return redirect('detalhes_pedido', pedido_id=item.pedido.id)
    else:
        form = ItemPedidoEditarForm(instance=item)
        # Calcular valor unitário após acréscimo/desconto e passar para o formulário
        if item.valor_total and item.quantidade:
            form.fields['valor_unitario'].initial = item.valor_total / item.quantidade
    
    return render(request, 'pedido/editar_item_pedido.html', {'form': form, 'item': item})

def excluir_item_pedido(request, item_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    item = get_object_or_404(Item_pedido, pk=item_id)
    
    if request.method == 'POST':
        pedido = item.pedido
        item.delete()
        
        # Recalcular o valor total do orçamento após excluir o item
        total_pedido = Item_pedido.objects.filter(pedido=pedido).aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        pedido.valor_total = total_pedido
        pedido.save()
        
        return redirect('detalhes_pedido', pedido_id=pedido.id)
    
    return render(request, 'pedido/excluir_item_pedido.html', {'item': item})


def editar_entrada_pedido(request, pedido_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    # Obter o objeto Pedido existente ou retornar 404 se não encontrado
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    if request.method == 'POST':
        # Obter o valor de entrada do formulário e converter para Decimal
        entrada_str = request.POST.get('entrada')
        entrada_decimal = Decimal(entrada_str)

        # Atualizar o valor de entrada do pedido
        pedido.entrada = entrada_decimal
        # Calcular o saldo subtraindo a entrada do valor total
        pedido.saldo = pedido.valor_total - pedido.entrada
        # Salvar as alterações no pedido
        pedido.save()

        # Redirecionar para a página de detalhes do pedido ou para onde desejar
        return redirect('detalhes_pedido', pedido_id=pedido.id)

    # Se não for um POST, exibir o formulário de edição do orçamento
    return render(request, 'pedido/editar_entrada_pedido.html', {'pedido': pedido})