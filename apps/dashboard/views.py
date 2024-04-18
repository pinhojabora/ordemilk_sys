from django.shortcuts import render, redirect
from django.contrib import messages
import matplotlib
matplotlib.use('Agg')
from apps.dashboard.models import Estatistica_geral, Estatistica_user
import matplotlib.pyplot as plt
import io
import base64
from django.contrib.auth.decorators import login_required
from apps.usuarios.models import Gerente, Vendedor, User

def dashboard(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
       
        return render(request, 'dashboard/index_dashboard.html')



def dashboard_geral(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    # Obter dados das estatísticas gerais e efetivação
    estatistica_geral = Estatistica_geral.objects.first()
    
    # Criar os dados para os subgráficos
    categorias = ['Configuração', 'Orçamento', 'Pedido']
    categoria2 = ['Efetivação']
    valores_gerais = [estatistica_geral.configuracao, estatistica_geral.orcamento, estatistica_geral.pedido]
    valores_efetivacao = [estatistica_geral.efetivacao]

    # Criar os subgráficos
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Subgráfico para as estatísticas gerais
    bars = axs[0].bar(categorias, valores_gerais, color='black')
    axs[0].set_title('Estatísticas Ordemilk')
    axs[0].set_ylabel('Valores')

    # Adicionar os valores sobre as barras no primeiro subgráfico
    for bar in bars:
        yval = bar.get_height()
        axs[0].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

    # Subgráfico para a efetivação
    bars_efetivacao = axs[1].bar(categoria2, valores_efetivacao, color='red')
    axs[1].set_title('Efetivação Ordemilk')
    axs[1].set_ylabel('Valores')

    # Adicionar o valor sobre a barra no segundo subgráfico
    for bar in bars_efetivacao:
        yval = bar.get_height()
        axs[1].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

    # Ajustes de layout
    plt.tight_layout()

    # Salvar a figura em BytesIO e converter para base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Passar a imagem para o template
    context = {'image_base64': image_base64}

    return render(request, 'dashboard/dashboard_geral.html', context)


def dashboard_vendedor(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    # Obter dados das estatísticas do usuário atual
    estatistica_user = Estatistica_user.objects.get(user=request.user)

    # Obter dados das estatísticas gerais
    estatistica_geral = Estatistica_geral.objects.first()
    
    # Criar os dados para os subgráficos do usuário
    categorias = ['Configuração', 'Orçamento', 'Pedido']
    valores_usuario = [estatistica_user.configuracao, estatistica_user.orcamento, estatistica_user.pedido]
    valores_efetivacao_usuario = [estatistica_user.efetivacao]

    # Criar os dados para os subgráficos das estatísticas gerais
    valores_gerais = [estatistica_geral.configuracao, estatistica_geral.orcamento, estatistica_geral.pedido]
    valores_efetivacao_geral = [estatistica_geral.efetivacao]

    # Criar os subgráficos
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Subgráfico para as estatísticas do usuário
    bars_usuario = axs[0].bar(categorias, valores_usuario, label='Vendedor', color='black')
    axs[0].set_title('Estatísticas do Vendedor')
    axs[0].set_ylabel('Valores')

    # Adicionar os valores sobre as barras no subgráfico do usuário
    for bar in bars_usuario:
        yval = bar.get_height()
        axs[0].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

    # Subgráfico para a efetivação do usuário
    bars_efetivacao_usuario = axs[1].bar(['Efetivação'], valores_efetivacao_usuario, label='Vendedor', color='black')
    axs[1].set_title('Efetivação do Vendedor')
    axs[1].set_ylabel('Valores')

    # Adicionar o valor sobre a barra no subgráfico de efetivação do usuário
    for bar in bars_efetivacao_usuario:
        yval = bar.get_height()
        axs[1].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

    # Adicionar as barras das estatísticas gerais nos subgráficos
    bars_gerais = axs[0].bar(categorias, valores_gerais, alpha=0.5, label='Ordemilk', color='red')
    bars_efetivacao_geral = axs[1].bar(['Efetivação'], valores_efetivacao_geral, alpha=0.5, label='Ordemilk', color='black')

    # Adicionar legenda aos subgráficos
    axs[0].legend()
    axs[1].legend()

    # Ajustes de layout
    plt.tight_layout()

    # Salvar a figura em BytesIO e converter para base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Passar a imagem para o template
    context = {'image_base64': image_base64}

    return render(request, 'dashboard/dashboard_vendedor.html', context)


@login_required
def dashboard_gerente(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    try:
        gerente = Gerente.objects.get(user=request.user)
    except Gerente.DoesNotExist:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard_usuario')  # Redirecionar para a página do usuário comum

    # Obter os vendedores vinculados a este gerente
    vendedores = Vendedor.objects.filter(gerente=gerente)

    # Criar os dados para os subgráficos dos vendedores
    categorias = ['Configuração', 'Orçamento', 'Pedido']
    fig, axs = plt.subplots(len(vendedores) + 1, 2, figsize=(12, (len(vendedores) + 1)*4))

    # Adicionar os dados do gerente
    try:
        estatistica_geral = Estatistica_geral.objects.first()
        valores_gerais = [estatistica_geral.configuracao, estatistica_geral.orcamento, estatistica_geral.pedido]

        bars_geral = axs[0, 0].bar(categorias, valores_gerais, color='black')
        axs[0, 0].set_title('Estatísticas Gerais')
        axs[0, 0].set_ylabel('Valores')

        for bar in bars_geral:
            yval = bar.get_height()
            axs[0, 0].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

        # Subplot para a efetivação geral
        bars_efetivacao_geral = axs[0, 1].bar(['Efetivação'], [estatistica_geral.efetivacao], color='red')
        axs[0, 1].set_title('Efetivação Geral')
        axs[0, 1].set_ylabel('Valores')

        for bar in bars_efetivacao_geral:
            yval = bar.get_height()
            axs[0, 1].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

    except Estatistica_geral.DoesNotExist:
        messages.warning(request, 'As estatísticas gerais não estão disponíveis.')

    for i, vendedor in enumerate(vendedores, start=1):  # Começando em 1 para evitar o subplot 0 já ocupado pelas estatísticas gerais
        try:
            estatistica_vendedor = Estatistica_user.objects.get(user=vendedor.user)
            valores_vendedor = [estatistica_vendedor.configuracao,
                                estatistica_vendedor.orcamento,
                                estatistica_vendedor.pedido]

            # Subplot para as estatísticas do vendedor
            bars_vendedor = axs[i, 0].bar(categorias, valores_vendedor, label=vendedor.user.username, color='black')
            axs[i, 0].set_title(f'Estatísticas de {vendedor.user.username}')
            axs[i, 0].set_ylabel('Valores')

            for bar in bars_vendedor:
                yval = bar.get_height()
                axs[i, 0].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

            # Subplot para a efetivação do vendedor
            bars_efetivacao_vendedor = axs[i, 1].bar(['Efetivação'], [estatistica_vendedor.efetivacao], color='red')
            axs[i, 1].set_title(f'Efetivação de {vendedor.user.username}')
            axs[i, 1].set_ylabel('Valores')

            for bar in bars_efetivacao_vendedor:
                yval = bar.get_height()
                axs[i, 1].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

        except Estatistica_user.DoesNotExist:
            messages.warning(request, f'As estatísticas do vendedor {vendedor.user.username} não estão disponíveis.')

    # Ajustes de layout
    plt.tight_layout()

    # Salvar a figura em BytesIO e converter para base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Passar a imagem para o template
    context = {'image_base64': image_base64}

    return render(request, 'dashboard/dashboard_gerente.html', context)

@login_required
def dashboard_todos_usuarios(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    # Obter todos os usuários
    usuarios = User.objects.all()

    # Criar os dados para os subgráficos dos usuários
    categorias = ['Configuração', 'Orçamento', 'Pedido']
    fig, axs = plt.subplots(len(usuarios) + 1, 2, figsize=(12, (len(usuarios) + 1) * 4))

    # Adicionar os dados da estatística geral
    try:
        estatistica_geral = Estatistica_geral.objects.first()
        valores_gerais = [estatistica_geral.configuracao, estatistica_geral.orcamento, estatistica_geral.pedido]

        bars_geral = axs[0, 0].bar(categorias, valores_gerais, color='black')
        axs[0, 0].set_title('Estatísticas Ordemilk')
        axs[0, 0].set_ylabel('Valores')

        for bar in bars_geral:
            yval = bar.get_height()
            axs[0, 0].text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), va='bottom', ha='center')

        # Subplot para a efetivação geral
        bars_efetivacao_geral = axs[0, 1].bar(['Efetivação'], [estatistica_geral.efetivacao], color='red')
        axs[0, 1].set_title('Efetivação Ordemilk')
        axs[0, 1].set_ylabel('Valores')

        for bar in bars_efetivacao_geral:
            yval = bar.get_height()
            axs[0, 1].text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), va='bottom', ha='center')

    except Estatistica_geral.DoesNotExist:
        messages.warning(request, 'As estatísticas gerais não estão disponíveis.')

    for i, usuario in enumerate(usuarios, start=1):  # Começando em 1 para evitar o subplot 0 já ocupado pelas estatísticas gerais
        try:
            estatistica_usuario = Estatistica_user.objects.get(user=usuario)
            valores_usuario = [estatistica_usuario.configuracao,
                               estatistica_usuario.orcamento,
                               estatistica_usuario.pedido]

            # Subplot para as estatísticas do usuário
            bars_usuario = axs[i, 0].bar(categorias, valores_usuario, label=usuario.username, color='black')
            axs[i, 0].set_title(f'Estatísticas de {usuario.username}')
            axs[i, 0].set_ylabel('Valores')

            for bar in bars_usuario:
                yval = bar.get_height()
                axs[i, 0].text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), va='bottom', ha='center')

            # Subplot para a efetivação do usuário
            bars_efetivacao_usuario = axs[i, 1].bar(['Efetivação'], [estatistica_usuario.efetivacao], color='red')
            axs[i, 1].set_title(f'Efetivação de {usuario.username}')
            axs[i, 1].set_ylabel('Valores')

            for bar in bars_efetivacao_usuario:
                yval = bar.get_height()
                axs[i, 1].text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), va='bottom', ha='center')

        except Estatistica_user.DoesNotExist:
            messages.warning(request, f'As estatísticas do usuário {usuario.username} não estão disponíveis.')

    # Ajustes de layout
    plt.tight_layout()

    # Salvar a figura em BytesIO e converter para base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Passar a imagem para o template
    context = {'image_base64': image_base64}

    return render(request, 'dashboard/dashboard_todos_usuarios.html', context)