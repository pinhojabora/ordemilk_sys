from django.shortcuts import render, redirect, get_object_or_404

from apps.configurador.forms import ConfiguradorForms, ItemConfiguradorForm, AtivaGerenciamentoForm, SelecionaGerenciamentoForm

from django.contrib import messages
from apps.configurador.models import Configurador, Item_configurador
from apps.produto.models import Produto
from apps.ferramentas.models import Tipo_contencao
from apps.orcamento.models import Orcamento, Item_orcamento
from apps.dashboard.models import Estatistica_user, Estatistica_geral
from apps.orcamento.views import lista_orcamento
from apps.dashboard.models import Estatistica_user
from datetime import datetime, timedelta
from django.http import HttpResponse

from decimal import Decimal

def lista_configurador(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        configuradores = Configurador.objects.all()
        return render(request, 'configurador/index_configurador.html',{"configuradores":configuradores})

def cadastro_configurador(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = ConfiguradorForms(request.POST)
        if form.is_valid():
            configurador = form.save(commit=False)
            configurador.usuario = request.user

            # Importa o fator_calculo do modelo_equipamento
            if configurador.modelo_equipamento:
                configurador.fator_calculo_modelo = configurador.modelo_equipamento.fator_calculo

            configurador.save()

            # Atualiza as estatísticas do usuário
            estatistica_user = Estatistica_user.objects.get_or_create(user=request.user)[0]
            estatistica_user.configuracao += 1
            estatistica_user.save()

            # Atualiza as estatísticas gerais
            estatistica_geral = Estatistica_geral.objects.first()
            estatistica_geral.configuracao += 1
            estatistica_geral.save()

            messages.success(request, 'Configuração cadastrada com sucesso!')
            return redirect('index_configurador')
        else:
            messages.error(request, 'Erro ao cadastrar a configuração. Por favor, verifique os dados informados.')
    else:
        form = ConfiguradorForms()
    return render(request, 'configurador/cadastro_configurador.html', {'form': form})

def editar_configuracao(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')

    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador = Configurador.objects.get(id=configurador_id)
    form = ConfiguradorForms(instance=configurador)
    if configurador.modelo_equipamento:
                configurador.fator_calculo_modelo = configurador.modelo_equipamento.fator_calculo

                configurador.save()
    if request.method == 'POST':
        form = ConfiguradorForms(request.POST, request.FILES, instance=configurador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuração editada com sucesso')
            return redirect('index_configurador')

    return render(request, 'configurador/editar_configurador.html', {'form': form, 'configurador_id': configurador_id})



def detalhes_configurador(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')

    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador_detalhado = Configurador.objects.get(pk=configurador_id)
    itens_configurador = Item_configurador.objects.filter(configurador=configurador_detalhado)
    return render(request, 'configurador/detalhes_configurador.html', {'configurador': configurador_detalhado, 'itens_configurador': itens_configurador})



def adicionar_item_configurador(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if request.method == 'POST':
        form = ItemConfiguradorForm(request.POST)
        if form.is_valid():
            configurador_id = form.cleaned_data['configurador_id']
            produto_id = form.cleaned_data['produto_id']
            
            if isinstance(configurador_id, str):
                # Remove o separador de milhares do configurador_id, se houver
                configurador_id = configurador_id.replace('.', '')

        # Verifica se produto_id é uma string antes de tentar substituir
            if isinstance(produto_id, str):
                # Remove o separador de milhares do produto_id, se houver
                produto_id = produto_id.replace('.', '')
            try:
                configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
                produto_id = int(produto_id)  # Converte o produto_id para um inteiro
            except ValueError:
                messages.error(request, 'IDs inválidos.')
                return redirect('seu_template')

            configurador = get_object_or_404(Configurador, pk=configurador_id)
            produto = get_object_or_404(Produto, pk=produto_id)
            
            # Crie um novo item de configurador com o produto selecionado
            novo_item = Item_configurador(configurador=configurador, produto=produto, quantidade=1)
            novo_item.save()
            configurador.valor_total += novo_item.valor_total
            configurador.save()

            return redirect('detalhes_configurador', configurador_id=configurador_id)
    else:
        form = ItemConfiguradorForm()

    return render(request, 'seu_template.html', {'form': form})

def configurador_contencao(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')

    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador = get_object_or_404(Configurador, pk=configurador_id)
    itens_configurador = Item_configurador.objects.filter(configurador=configurador)

    # Obtenha os produtos relacionados à contenção da configuração
    produtos_contencao = Produto.objects.filter(tipo_contencao=configurador.tipo_contencao, modelo_sala=configurador.modelo_sala)

    return render(request, 'configurador/contencao.html', {
        'configurador': configurador,
        'itens_configurador': itens_configurador,
        'produtos_contencao': produtos_contencao,  # Passa os produtos relacionados à contenção para o template
    })

def adicionar_contencao(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if request.method == 'POST':
        form = ItemConfiguradorForm(request.POST)
        if form.is_valid():
            configurador_id = form.cleaned_data['configurador_id']
            produto_id = form.cleaned_data['produto_id']
            
            if isinstance(configurador_id, str):
                # Remove o separador de milhares do configurador_id, se houver
                configurador_id = configurador_id.replace('.', '')

        # Verifica se produto_id é uma string antes de tentar substituir
            if isinstance(produto_id, str):
                # Remove o separador de milhares do produto_id, se houver
                produto_id = produto_id.replace('.', '')

            try:
                configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
                produto_id = int(produto_id)  # Converte o produto_id para um inteiro
            except ValueError:
                messages.error(request, 'IDs inválidos.')
                return redirect('seu_template')

            configurador = get_object_or_404(Configurador, pk=configurador_id)
            produto = get_object_or_404(Produto, pk=produto_id)
            
            # Crie um novo item de configurador com o produto selecionado
            novo_item = Item_configurador(configurador=configurador,
                                          produto=produto, 
                                          quantidade=1, 
                                          valor_unitario=produto.preco_com_ipi, 
                                          valor_total=produto.preco_com_ipi)
            novo_item.save()
            configurador.valor_total += novo_item.valor_total
            configurador.save()

            return redirect('configurador_unidade_final', configurador_id=configurador_id)
    else:
        form = ItemConfiguradorForm()

    return render(request, 'seu_template.html', {'form': form})

def configurador_unidade_final(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')

    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador = get_object_or_404(Configurador, pk=configurador_id)
    itens_configurador = Item_configurador.objects.filter(configurador=configurador)

    # Obtenha os produtos relacionados à unidade final da configuração
    produtos_unidade_final = Produto.objects.filter(modelo_sala=configurador.modelo_sala, modelo_equipamento=configurador.modelo_equipamento, tipo_linha=configurador.tipo_linha)

    return render(request, 'configurador/unidade_final.html', {
        'configurador': configurador,
        'itens_configurador': itens_configurador,
        'produtos_unidade_final': produtos_unidade_final,  # Passa os produtos relacionados à unidade final para o template
    })

def adicionar_unidade_final(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if request.method == 'POST':
        form = ItemConfiguradorForm(request.POST)
        if form.is_valid():
            configurador_id = form.cleaned_data['configurador_id']
            produto_id = form.cleaned_data['produto_id']
            
            if isinstance(configurador_id, str):
                # Remove o separador de milhares do configurador_id, se houver
                configurador_id = configurador_id.replace('.', '')

        # Verifica se produto_id é uma string antes de tentar substituir
            if isinstance(produto_id, str):
                # Remove o separador de milhares do produto_id, se houver
                produto_id = produto_id.replace('.', '')

            try:
                configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
                produto_id = int(produto_id)  # Converte o produto_id para um inteiro
            except ValueError:
                messages.error(request, 'IDs inválidos.')
                return redirect('seu_template')

            configurador = get_object_or_404(Configurador, pk=configurador_id)
            produto = get_object_or_404(Produto, pk=produto_id)
            
            # Crie um novo item de configurador com o produto selecionado
            novo_item = Item_configurador(configurador=configurador,
                                          produto=produto, 
                                          quantidade=1, 
                                          valor_unitario=produto.preco_com_ipi, 
                                          valor_total=produto.preco_com_ipi)
            novo_item.save()
            configurador.valor_total += novo_item.valor_total
            configurador.numero_conjuntos = produto.numero_conjuntos
            configurador.save()

            return redirect('configurador_sistema_limpeza', configurador_id=configurador_id)
    else:
        form = ItemConfiguradorForm()

    return render(request, 'seu_template.html', {'form': form})


def configurador_sistema_limpeza(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')

    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador = get_object_or_404(Configurador, pk=configurador_id)
    itens_configurador = Item_configurador.objects.filter(configurador=configurador)

    # Obtenha os produtos relacionados ao sistema de limpeza da configuração
    produtos_sistema_limpeza = Produto.objects.filter(sistema_limpeza=True)

    return render(request, 'configurador/sistema_limpeza.html', {
        'configurador': configurador,
        'itens_configurador': itens_configurador,
        'produtos_sistema_limpeza': produtos_sistema_limpeza,  # Passa os produtos relacionados ao sistema de limpeza para o template
    })

def adicionar_sistema_limpeza(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if request.method == 'POST':
        form = ItemConfiguradorForm(request.POST)
        if form.is_valid():
            configurador_id = form.cleaned_data['configurador_id']
            produto_id = form.cleaned_data['produto_id']
            
            if isinstance(configurador_id, str):
                # Remove o separador de milhares do configurador_id, se houver
                configurador_id = configurador_id.replace('.', '')

        # Verifica se produto_id é uma string antes de tentar substituir
            if isinstance(produto_id, str):
                # Remove o separador de milhares do produto_id, se houver
                produto_id = produto_id.replace('.', '')

            try:
                configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
                produto_id = int(produto_id)  # Converte o produto_id para um inteiro
            except ValueError:
                messages.error(request, 'IDs inválidos.')
                return redirect('seu_template')

            configurador = get_object_or_404(Configurador, pk=configurador_id)
            produto = get_object_or_404(Produto, pk=produto_id)
            
            # Crie um novo item de configurador com o produto selecionado
            novo_item = Item_configurador(configurador=configurador,
                                          produto=produto, 
                                          quantidade=1, 
                                          valor_unitario=produto.preco_com_ipi, 
                                          valor_total=produto.preco_com_ipi)
            novo_item.save()
            configurador.valor_total += novo_item.valor_total
            configurador.save()

            return redirect('configurador_unidade_vacuo', configurador_id=configurador_id)
    else:
        form = ItemConfiguradorForm()

    return render(request, 'seu_template.html', {'form': form})



def configurador_unidade_vacuo(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')

    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador = get_object_or_404(Configurador, pk=configurador_id)
    itens_configurador = Item_configurador.objects.filter(configurador=configurador)

    # Calcular o vacuo recomendado
    configurador.vacuo_recomendado = ((configurador.numero_conjuntos * 80) + configurador.fator_calculo_modelo) * configurador.altitude
    configurador.save()
    # Obtenha os produtos relacionados à unidade de vácuo da configuração
    produtos_unidade_vacuo = Produto.objects.filter(
        tensao_energia=configurador.tensao_energia,
        maximo_vacuo__gt=configurador.vacuo_recomendado
    )

    return render(request, 'configurador/unidade_vacuo.html', {
        'configurador': configurador,
        'itens_configurador': itens_configurador,
        'produtos_unidade_vacuo': produtos_unidade_vacuo,  # Passa os produtos relacionados à unidade de vácuo para o template
    })

def adicionar_unidade_vacuo(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if request.method == 'POST':
        form = ItemConfiguradorForm(request.POST)
        if form.is_valid():
            configurador_id = form.cleaned_data['configurador_id']
            produto_id = form.cleaned_data['produto_id']
            
            if isinstance(configurador_id, str):
                # Remove o separador de milhares do configurador_id, se houver
                configurador_id = configurador_id.replace('.', '')

        # Verifica se produto_id é uma string antes de tentar substituir
            if isinstance(produto_id, str):
                # Remove o separador de milhares do produto_id, se houver
                produto_id = produto_id.replace('.', '')

            try:
                configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
                produto_id = int(produto_id)  # Converte o produto_id para um inteiro
            except ValueError:
                messages.error(request, 'IDs inválidos.')
                return redirect('seu_template')

            configurador = get_object_or_404(Configurador, pk=configurador_id)
            produto = get_object_or_404(Produto, pk=produto_id)
            
            # Crie um novo item de configurador com o produto selecionado
            novo_item = Item_configurador(configurador=configurador,
                                          produto=produto, 
                                          quantidade=1, 
                                          valor_unitario=produto.preco_com_ipi, 
                                          valor_total=produto.preco_com_ipi)
            novo_item.save()
            configurador.valor_total += novo_item.valor_total
            configurador.save()

            return redirect('ativa_gerenciamento', configurador_id=configurador_id)
    else:
        form = ItemConfiguradorForm()

    return render(request, 'seu_template.html', {'form': form})


def ativa_gerenciamento(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')
    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador = Configurador.objects.get(id=configurador_id)
    form = AtivaGerenciamentoForm(instance=configurador)

    if request.method == 'POST':
        form = AtivaGerenciamentoForm(request.POST, request.FILES, instance=configurador)
        if form.is_valid():
            print(request.POST)
            form.save()
            messages.success(request, 'Configuração editada com sucesso')
            return redirect('seleciona_gerenciamento', configurador_id=configurador_id)

    return render(request, 'configurador/ativa_gerenciamento.html', {'form': form, 'configurador_id': configurador_id})

def seleciona_gerenciamento(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')

    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador = Configurador.objects.get(id=configurador_id)
    form = SelecionaGerenciamentoForm(instance=configurador)

    if request.method == 'POST':
        form = SelecionaGerenciamentoForm(request.POST, request.FILES, instance=configurador)
        if form.is_valid():
            print(request.POST)
            form.save()
            messages.success(request, 'Configuração editada com sucesso')
            return redirect('configurador_nobreak', configurador_id=configurador_id)

    return render(request, 'configurador/seleciona_gerenciamento.html', {'form': form, 'configurador_id': configurador_id})

def configurador_extrator(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')

    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador = get_object_or_404(Configurador, pk=configurador_id)
    itens_configurador = Item_configurador.objects.filter(configurador=configurador)

    # Obtenha os produtos relacionados ao extrator da configuração
    produtos_extrator = Produto.objects.filter(modelo_equipamento=configurador.modelo_equipamento, tipo_linha=configurador.tipo_linha, extracao=True, numero_conjuntos__gt=configurador.numero_conjuntos)

    return render(request, 'configurador/extrator.html', {
        'configurador': configurador,
        'itens_configurador': itens_configurador,
        'produtos_extrator': produtos_extrator,  # Passa os produtos relacionados ao extrator para o template
    })

def adicionar_extrator(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if request.method == 'POST':
        form = ItemConfiguradorForm(request.POST)
        if form.is_valid():
            configurador_id = form.cleaned_data['configurador_id']
            produto_id = form.cleaned_data['produto_id']
            
            if isinstance(configurador_id, str):
                # Remove o separador de milhares do configurador_id, se houver
                configurador_id = configurador_id.replace('.', '')

        # Verifica se produto_id é uma string antes de tentar substituir
            if isinstance(produto_id, str):
                # Remove o separador de milhares do produto_id, se houver
                produto_id = produto_id.replace('.', '')

            try:
                configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
                produto_id = int(produto_id)  # Converte o produto_id para um inteiro
            except ValueError:
                messages.error(request, 'IDs inválidos.')
                return redirect('seu_template')

            configurador = get_object_or_404(Configurador, pk=configurador_id)
            produto = get_object_or_404(Produto, pk=produto_id)
            
            # Crie um novo item de configurador com o produto selecionado
            novo_item = Item_configurador(configurador=configurador,
                                          produto=produto, 
                                          quantidade=1, 
                                          valor_unitario=produto.preco_com_ipi, 
                                          valor_total=produto.preco_com_ipi)
            novo_item.save()
            configurador.valor_total += novo_item.valor_total
            configurador.save()

            return redirect('configurador_conj_ordenha', configurador_id=configurador_id)
    else:
        form = ItemConfiguradorForm()

    return render(request, 'seu_template.html', {'form': form})


def configurador_conj_ordenha(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')

    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador = get_object_or_404(Configurador, pk=configurador_id)
    itens_configurador = Item_configurador.objects.filter(configurador=configurador)

    # Obtenha os produtos relacionados ao conjunto de ordenha da configuração
    produtos_conj_ordenha = Produto.objects.filter(conj_ordenha=True)

    return render(request, 'configurador/conjunto_ordenha.html', {
        'configurador': configurador,
        'itens_configurador': itens_configurador,
        'produtos_conj_ordenha': produtos_conj_ordenha,  # Passa os produtos relacionados ao conjunto de ordenha para o template
    })

def adicionar_conj_ordenha(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if request.method == 'POST':
        form = ItemConfiguradorForm(request.POST)
        if form.is_valid():
            configurador_id = form.cleaned_data['configurador_id']
            produto_id = form.cleaned_data['produto_id']
            
            if isinstance(configurador_id, str):
                # Remove o separador de milhares do configurador_id, se houver
                configurador_id = configurador_id.replace('.', '')

        # Verifica se produto_id é uma string antes de tentar substituir
            if isinstance(produto_id, str):
                # Remove o separador de milhares do produto_id, se houver
                produto_id = produto_id.replace('.', '')

            try:
                configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
                produto_id = int(produto_id)  # Converte o produto_id para um inteiro
            except ValueError:
                messages.error(request, 'IDs inválidos.')
                return redirect('seu_template')

            configurador = get_object_or_404(Configurador, pk=configurador_id)
            produto = get_object_or_404(Produto, pk=produto_id)
            
            # Crie um novo item de configurador com o produto selecionado
            novo_item = Item_configurador(configurador=configurador,
                                          produto=produto, 
                                          quantidade=1, 
                                          valor_unitario=produto.preco_com_ipi, 
                                          valor_total=produto.preco_com_ipi)
            novo_item.save()
            configurador.valor_total += novo_item.valor_total
            configurador.save()

            return redirect('ativa_gerenciamento', configurador_id=configurador_id)
    else:
        form = ItemConfiguradorForm()

    return render(request, 'seu_template.html', {'form': form})

def configurador_nobreak(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if isinstance(configurador_id, str):
        # Remove o separador de milhares do configurador_id, se houver
        configurador_id = configurador_id.replace('.', '')

    try:
        configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
    except ValueError:
        messages.error(request, 'ID do configurador inválido.')
        return redirect('index_configurador')

    configurador = get_object_or_404(Configurador, pk=configurador_id)
    itens_configurador = Item_configurador.objects.filter(configurador=configurador)

    # Obtenha os produtos relacionados à unidade final da configuração
    produtos_nobreak = Produto.objects.filter(nobreak=True)

    return render(request, 'configurador/nobreak.html', {
        'configurador': configurador,
        'itens_configurador': itens_configurador,
        'produtos_nobreak': produtos_nobreak,  # Passa os produtos relacionados à unidade final para o template
    })

def adicionar_nobreak(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    if request.method == 'POST':
        form = ItemConfiguradorForm(request.POST)
        if form.is_valid():
            configurador_id = form.cleaned_data['configurador_id']
            produto_id = form.cleaned_data['produto_id']
            
            if isinstance(configurador_id, str):
                # Remove o separador de milhares do configurador_id, se houver
                configurador_id = configurador_id.replace('.', '')

        # Verifica se produto_id é uma string antes de tentar substituir
            if isinstance(produto_id, str):
                # Remove o separador de milhares do produto_id, se houver
                produto_id = produto_id.replace('.', '')

            try:
                configurador_id = int(configurador_id)  # Converte o configurador_id para um inteiro
                produto_id = int(produto_id)  # Converte o produto_id para um inteiro
            except ValueError:
                messages.error(request, 'IDs inválidos.')
                return redirect('seu_template')

            configurador = get_object_or_404(Configurador, pk=configurador_id)
            produto = get_object_or_404(Produto, pk=produto_id)
            
            # Crie um novo item de configurador com o produto selecionado
            novo_item = Item_configurador(configurador=configurador,
                                          produto=produto, 
                                          quantidade=1, 
                                          valor_unitario=produto.preco_com_ipi, 
                                          valor_total=produto.preco_com_ipi)
            novo_item.save()
            
            configurador.valor_total += novo_item.valor_total
            configurador.save()
            
            return redirect('detalhes_configurador', configurador_id=configurador_id)
    else:
        form = ItemConfiguradorForm()

    return render(request, 'seu_template.html', {'form': form})


def calcular_efetivacao(orcamento, pedido):
    orcamento_decimal = Decimal(orcamento)
    pedido_decimal = Decimal(pedido)
    
    if orcamento_decimal == Decimal(0):
        return Decimal(0)
    
    return ((pedido_decimal - orcamento_decimal) / orcamento_decimal) * Decimal(100)

def converter_configuracao_orcamento(request, configurador_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    try:
        if isinstance(configurador_id, str):
                # Remove o separador de milhares do configurador_id, se houver
                configurador_id = configurador_id.replace('.', '')

        # Verifica se produto_id é uma string antes de tentar substituir
        if isinstance(produto_id, str):
                # Remove o separador de milhares do produto_id, se houver
                produto_id = produto_id.replace('.', '')

        configurador = Configurador.objects.get(pk=configurador_id)

        # Criar o orçamento com base nos dados do configurador
        novo_orcamento = Orcamento.objects.create(
            data_orcamento=configurador.data_configuracao,
            nome_cliente=configurador.nome_cliente,
            endereco_cliente=configurador.endereco_cliente,
            cidade=configurador.cidade,
            estado=configurador.estado,
            cep=configurador.cep,
            cnpj_cpf=configurador.cnpj_cpf,
            insc_estadual=configurador.insc_estadual,
            fone=configurador.fone,
            email=configurador.email,
            observacao=configurador.observacao,
            usuario=configurador.usuario,
            vencimento_orcamento=configurador.data_configuracao + timedelta(days=30),
            dias_faltantes='30',
            valor_total=configurador.valor_total
        )

        # Copiar itens do orçamento para o pedido
        for item_configurador in configurador.item_configurador_set.all():
            Item_orcamento.objects.create(
                orcamento=novo_orcamento,
                produto=item_configurador.produto,
                quantidade=item_configurador.quantidade,
                valor_unitario=item_configurador.valor_unitario,
                valor_total=item_configurador.valor_total,
            )

        # Atualizar as estatísticas do usuário
        estatistica_user = Estatistica_user.objects.get_or_create(user=request.user)[0]
        estatistica_user.orcamento += 1
        estatistica_user.efetivacao = calcular_efetivacao(estatistica_user.orcamento, estatistica_user.pedido)
        estatistica_user.save()

        # Atualizar as estatísticas gerais
        estatistica_geral = Estatistica_geral.objects.first()
        estatistica_geral.orcamento += 1
        estatistica_geral.efetivacao = calcular_efetivacao(estatistica_geral.orcamento, estatistica_geral.pedido)
        estatistica_geral.save()

        # Excluir o orçamento após a conversão em pedido
        configurador.delete()

        # Exibir mensagem de sucesso
        messages.success(request, 'Configuração convertida em orçamento com sucesso!')
        return redirect(lista_orcamento)

    except Exception as e:
        # Exibir mensagem de erro
        messages.error(request, f'Erro ao converter configuração em orçamento: {e}')

    # Redirecionar de volta para a página de index de orçamentos
    return redirect('index_configurador')