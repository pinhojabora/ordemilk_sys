from django.shortcuts import render, redirect

from apps.produto.forms import ProdutoForms

from django.contrib import messages

from apps.produto.models import produto


def lista_produto(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        produtos = produto.objects.all()
        return render(request, 'produto/produto.html',{"produtos":produtos})

def cadastro_produto(request):
    if request.method == 'POST':
        form = ProdutoForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('produto')
        else:
            messages.error(request, 'Erro ao cadastrar o produto. Por favor, verifique os dados informados.')
    else:
        form = ProdutoForms()
    return render(request, 'produto/cadastro_produto.html', {'form': form})

def detalhes_produto(request, produto_id):
    produto_detalhado = produto.objects.get(pk=produto_id)
    return render(request, 'produto/detalhes_produto.html', {'produto': produto_detalhado})

def buscar(request):
     if "buscar" in request.GET:
        nome_a_buscar=request.GET['buscar']
        if nome_a_buscar:
             produtos = produto.objects.filter(nome__icontains=nome_a_buscar)
                

        return render(request, 'produto/buscar.html', {"produtos":produtos})