from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from apps.ferramentas.forms import Tensao_energiaForms, Modelo_salaForms, Modelo_equipamentoForms, Tipo_linhaForms, Tipo_contencaoForms, Tipo_gerenciamentoForms

from apps.ferramentas.models import Tensao_energia, Modelo_sala, Modelo_equipamento, Tipo_linha, Tipo_contencao, Tipo_gerenciamento

def index_ferramentas(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
        
        return render(request, 'ferramentas/index_ferramentas.html')

def cadastro_tensao_energia(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = Tensao_energiaForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tensão cadastrada com sucesso!')
            return redirect('index_tensao')
        else:
            messages.error(request, 'Erro ao cadastrar a tensão. Por favor, verifique os dados informados.')
    else:
        form = Tensao_energiaForms()
    return render(request, 'ferramentas/cadastro_tensao.html', {'form': form})

def lista_tensao_energia(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        tensao_energias = Tensao_energia.objects.all()
        return render(request, 'ferramentas/index_tensao.html',{"tensao_energias":tensao_energias})


def editar_tensao_energia(request, tensao_energia_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    tensao_energia = get_object_or_404(Tensao_energia, id=tensao_energia_id)
    form = Tensao_energiaForms(instance=tensao_energia)

    if request.method == 'POST':
        form = Tensao_energiaForms(request.POST, request.FILES, instance=tensao_energia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tensão editada com sucesso')
            return redirect('index_tensao')

    return render(request, 'ferramentas/editar_tensao.html', {'form': form, 'tensao_energia_id': tensao_energia_id})


def excluir_tensao_energia(request, tensao_energia_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    tensao_energia = get_object_or_404(Tensao_energia, pk=tensao_energia_id)
    
    if request.method == 'POST':
        # Verifica se o usuário confirmou a exclusão do pedido
        if 'confirmacao' in request.POST:
            tensao_energia.delete()
            messages.success(request, 'Tensão excluída com sucesso!')
            return redirect(lista_tensao_energia)  # Redireciona para a página de index de pedidos ou outra página desejada após a exclusão
        else:
            messages.error(request, 'Você não confirmou a exclusão.')
            return redirect('index_tensao')  # Redireciona de volta para a página de detalhes do pedido
        
    return render(request, 'ferramentas/excluir_tensao.html', {'tensao_energia': tensao_energia})

def cadastro_modelo_sala(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = Modelo_salaForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo de sala cadastrada com sucesso!')
            return redirect('index_sala')
        else:
            messages.error(request, 'Erro ao cadastrar o modelo de sala. Por favor, verifique os dados informados.')
    else:
        form = Modelo_salaForms()
    return render(request, 'ferramentas/cadastro_sala.html', {'form': form})

def lista_modelo_sala(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        modelo_salas = Modelo_sala.objects.all()
        return render(request, 'ferramentas/index_sala.html',{"modelo_salas":modelo_salas})


def editar_modelo_sala(request, modelo_sala_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    modelo_sala = get_object_or_404(Modelo_sala, id=modelo_sala_id)
    form = Modelo_salaForms(instance=modelo_sala)

    if request.method == 'POST':
        form = Modelo_salaForms(request.POST, request.FILES, instance=modelo_sala)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo de sala editada com sucesso')
            return redirect('index_sala')

    return render(request, 'ferramentas/editar_sala.html', {'form': form, 'modelo_sala_id': modelo_sala_id})


def excluir_modelo_sala(request, modelo_sala_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    modelo_sala = get_object_or_404(Modelo_sala, pk=modelo_sala_id)
    
    if request.method == 'POST':
        # Verifica se o usuário confirmou a exclusão do pedido
        if 'confirmacao' in request.POST:
            modelo_sala.delete()
            messages.success(request, 'Modelo de sala excluído com sucesso!')
            return redirect(lista_modelo_sala)  # Redireciona para a página de index de pedidos ou outra página desejada após a exclusão
        else:
            messages.error(request, 'Você não confirmou a exclusão.')
            return redirect('index_sala')  # Redireciona de volta para a página de detalhes do pedido
        
    return render(request, 'ferramentas/excluir_sala.html', {'modelo_sala': modelo_sala})

def cadastro_modelo_equipamento(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = Modelo_equipamentoForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo de equipamento cadastrada com sucesso!')
            return redirect('index_equipamento')
        else:
            messages.error(request, 'Erro ao cadastrar o modelo de equipamento. Por favor, verifique os dados informados.')
    else:
        form = Modelo_equipamentoForms()
    return render(request, 'ferramentas/cadastro_equipamento.html', {'form': form})

def lista_modelo_equipamento(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        modelo_equipamentos = Modelo_equipamento.objects.all()
        return render(request, 'ferramentas/index_equipamento.html',{"modelo_equipamentos":modelo_equipamentos})


def editar_modelo_equipamento(request, modelo_equipamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    modelo_equipamento = get_object_or_404(Modelo_equipamento, id=modelo_equipamento_id)
    form = Modelo_equipamentoForms(instance=modelo_equipamento)

    if request.method == 'POST':
        form = Modelo_equipamentoForms(request.POST, request.FILES, instance=modelo_equipamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo de equipamento editado com sucesso')
            return redirect('index_equipamento')

    return render(request, 'ferramentas/editar_equipamento.html', {'form': form, 'modelo_equipamento_id': modelo_equipamento_id})


def excluir_modelo_equipamento(request, modelo_equipamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    modelo_equipamento = get_object_or_404(Modelo_equipamento, pk=modelo_equipamento_id)
    
    if request.method == 'POST':
        # Verifica se o usuário confirmou a exclusão do pedido
        if 'confirmacao' in request.POST:
            modelo_equipamento.delete()
            messages.success(request, 'Modelo de equipamento excluído com sucesso!')
            return redirect(lista_modelo_equipamento)  # Redireciona para a página de index de pedidos ou outra página desejada após a exclusão
        else:
            messages.error(request, 'Você não confirmou a exclusão.')
            return redirect('index_equipamento')  # Redireciona de volta para a página de detalhes do pedido
        
    return render(request, 'ferramentas/excluir_equipamento.html', {'modelo_equipamento': modelo_equipamento})

def cadastro_tipo_linha(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = Tipo_linhaForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de linha cadastrado com sucesso!')
            return redirect('index_linha')
        else:
            messages.error(request, 'Erro ao cadastrar o tipo de linha. Por favor, verifique os dados informados.')
    else:
        form = Tipo_linhaForms()
    return render(request, 'ferramentas/cadastro_linha.html', {'form': form})

def lista_tipo_linha(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        tipo_linhas = Tipo_linha.objects.all()
        return render(request, 'ferramentas/index_linha.html',{"tipo_linhas":tipo_linhas})


def editar_tipo_linha(request, tipo_linha_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    tipo_linha = get_object_or_404(Tipo_linha, id=tipo_linha_id)
    form = Tipo_linhaForms(instance=tipo_linha)

    if request.method == 'POST':
        form = Tipo_linhaForms(request.POST, request.FILES, instance=tipo_linha)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de linha editado com sucesso')
            return redirect('index_linha')

    return render(request, 'ferramentas/editar_linha.html', {'form': form, 'tipo_linha_id': tipo_linha_id})


def excluir_tipo_linha(request, tipo_linha_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    tipo_linha = get_object_or_404(Tipo_linha, pk=tipo_linha_id)
    
    if request.method == 'POST':
        # Verifica se o usuário confirmou a exclusão do pedido
        if 'confirmacao' in request.POST:
            tipo_linha.delete()
            messages.success(request, 'Tipo de linha excluído com sucesso!')
            return redirect(lista_tipo_linha)  # Redireciona para a página de index de pedidos ou outra página desejada após a exclusão
        else:
            messages.error(request, 'Você não confirmou a exclusão.')
            return redirect('index_linha')  # Redireciona de volta para a página de detalhes do pedido
        
    return render(request, 'ferramentas/excluir_linha.html', {'tipo_linha': tipo_linha})

def cadastro_tipo_contencao(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = Tipo_contencaoForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de contencao cadastrado com sucesso!')
            return redirect('index_contencao')
        else:
            messages.error(request, 'Erro ao cadastrar o tipo de contencao. Por favor, verifique os dados informados.')
    else:
        form = Tipo_contencaoForms()
    return render(request, 'ferramentas/cadastro_contencao.html', {'form': form})

def lista_tipo_contencao(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        tipo_contencaos = Tipo_contencao.objects.all()
        return render(request, 'ferramentas/index_contencao.html',{"tipo_contencaos":tipo_contencaos})


def editar_tipo_contencao(request, tipo_contencao_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    tipo_contencao = get_object_or_404(Tipo_contencao, id=tipo_contencao_id)
    form = Tipo_contencaoForms(instance=tipo_contencao)

    if request.method == 'POST':
        form = Tipo_contencaoForms(request.POST, request.FILES, instance=tipo_contencao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de contencao editado com sucesso')
            return redirect('index_contencao')

    return render(request, 'ferramentas/editar_contencao.html', {'form': form, 'tipo_contencao_id': tipo_contencao_id})


def excluir_tipo_contencao(request, tipo_contencao_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    tipo_contencao = get_object_or_404(Tipo_contencao, pk=tipo_contencao_id)
    
    if request.method == 'POST':
        # Verifica se o usuário confirmou a exclusão do pedido
        if 'confirmacao' in request.POST:
            tipo_contencao.delete()
            messages.success(request, 'Tipo de contencao excluído com sucesso!')
            return redirect(lista_tipo_contencao)  # Redireciona para a página de index de pedidos ou outra página desejada após a exclusão
        else:
            messages.error(request, 'Você não confirmou a exclusão.')
            return redirect('index_contencao')  # Redireciona de volta para a página de detalhes do pedido
        
    return render(request, 'ferramentas/excluir_contencao.html', {'tipo_contencao': tipo_contencao})

def cadastro_tipo_gerenciamento(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = Tipo_gerenciamentoForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de gerenciamento cadastrado com sucesso!')
            return redirect('index_gerenciamento')
        else:
            messages.error(request, 'Erro ao cadastrar o tipo de gerenciamento. Por favor, verifique os dados informados.')
    else:
        form = Tipo_gerenciamentoForms()
    return render(request, 'ferramentas/cadastro_gerenciamento.html', {'form': form})

def lista_tipo_gerenciamento(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        tipo_gerenciamentos = Tipo_gerenciamento.objects.all()
        return render(request, 'ferramentas/index_gerenciamento.html',{"tipo_gerenciamentos":tipo_gerenciamentos})


def editar_tipo_gerenciamento(request, tipo_gerenciamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    tipo_gerenciamento = get_object_or_404(Tipo_gerenciamento, id=tipo_gerenciamento_id)
    form = Tipo_gerenciamentoForms(instance=tipo_gerenciamento)

    if request.method == 'POST':
        form = Tipo_gerenciamentoForms(request.POST, request.FILES, instance=tipo_gerenciamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de gerenciamento editado com sucesso')
            return redirect('index_gerenciamento')

    return render(request, 'ferramentas/editar_gerenciamento.html', {'form': form, 'tipo_gerenciamento_id': tipo_gerenciamento_id})


def excluir_tipo_gerenciamento(request, tipo_gerenciamento_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    tipo_gerenciamento = get_object_or_404(Tipo_gerenciamento, pk=tipo_gerenciamento_id)
    
    if request.method == 'POST':
        # Verifica se o usuário confirmou a exclusão do pedido
        if 'confirmacao' in request.POST:
            tipo_gerenciamento.delete()
            messages.success(request, 'Tipo de gerenciamento excluído com sucesso!')
            return redirect(lista_tipo_gerenciamento)  # Redireciona para a página de index de pedidos ou outra página desejada após a exclusão
        else:
            messages.error(request, 'Você não confirmou a exclusão.')
            return redirect('index_gerenciamento')  # Redireciona de volta para a página de detalhes do pedido
        
    return render(request, 'ferramentas/excluir_gerenciamento.html', {'tipo_gerenciamento': tipo_gerenciamento})