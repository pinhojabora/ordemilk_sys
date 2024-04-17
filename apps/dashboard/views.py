from django.shortcuts import render
from django.contrib import messages
import matplotlib
matplotlib.use('Agg')
from apps.dashboard.models import Estatistica_geral
import matplotlib.pyplot as plt
import io
import base64

def dashboard(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
       
        return render(request, 'dashboard/index_dashboard.html')



def dashboard_geral(request):
    # Obter dados das estatísticas gerais
    estatistica_geral = Estatistica_geral.objects.first()

    # Extrair os valores de cada estatística
       
    categorias = ['Configuração', 'Orçamento', 'Pedido']
    valores = [estatistica_geral.configuracao, estatistica_geral.orcamento, estatistica_geral.pedido]
    
    # Criar o gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(categorias, valores)
    # Adicionar rótulos e título
    plt.xlabel('Categorias')
    plt.ylabel('Valores')
    plt.title('Estatísticas Gerais')

   
    # Salvar o gráfico em BytesIO e converter para base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Passar a imagem para o template
    context = {'image_base64': image_base64}

    return render(request, 'dashboard/dashboard_geral.html', context)