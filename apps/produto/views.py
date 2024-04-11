from django.shortcuts import render, redirect, get_object_or_404

from apps.produto.forms import ProdutoForms, CategoriaForms, SubcategoriaForms

from django.contrib import messages

from apps.produto.models import Produto, Categoria, Subcategoria
from django.http import HttpResponse
from django.db.models import Q

def lista_produto(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        produtos = Produto.objects.all().order_by('nome')  # Ordena os produtos por nome
        categorias = Categoria.objects.all().order_by('nome')  # Ordena as categorias por nome
        categoria_id = request.GET.get('categoria')

        if categoria_id:
            categoria_selecionada = Categoria.objects.get(id=categoria_id)
            produtos_categoria = Produto.objects.filter(categoria=categoria_selecionada).order_by('nome')  # Ordena os produtos por nome
        else:
            categoria_selecionada = '0'
            produtos_categoria = Produto.objects.all().order_by('nome')  # Ordena os produtos por nome

    # Agrupar os produtos por subcategoria
        produtos_agrupados = {}
        for produto in produtos_categoria:
                if produto.subcategoria not in produtos_agrupados:
                 produtos_agrupados[produto.subcategoria] = []
                 produtos_agrupados[produto.subcategoria].append(produto)

    # Ordenar o dicionário de produtos_agrupados pelas chaves (subcategorias)
        produtos_agrupados = dict(sorted(produtos_agrupados.items(), key=lambda x: x[0].nome if x[0] is not None else ''))

        return render(request, 'produto/produto.html', {
        'produtos_agrupados': produtos_agrupados,
        'categorias': categorias,
        'categoria_selecionada': categoria_selecionada,
    })

def cadastro_produto(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
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
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    produto_detalhado = Produto.objects.get(pk=produto_id)
    fotografias = produto_detalhado.fotografias.all()  # Acessando todas as fotografias associadas ao produto
    return render(request, 'produto/detalhes_produto.html', {'produto': produto_detalhado, 'fotografias': fotografias})


def buscar(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    if "buscar" in request.GET:
        termo_busca = request.GET['buscar']
        if termo_busca:
            # Filtra os produtos por nome ou código, ignorando maiúsculas e minúsculas
            produtos = Produto.objects.filter(Q(nome__icontains=termo_busca) | Q(codigo__icontains=termo_busca))
            
    return render(request, 'produto/buscar.html', {'produtos': produtos, 'termo_busca': termo_busca})
    


def editar_produto(request, produto_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    produtos = Produto.objects.get(id=produto_id)
    form = ProdutoForms(instance=produtos)

    if request.method == "POST":
         form = ProdutoForms(request.POST, request.FILES, instance=produtos)
         if form.is_valid():
              print(request.POST)
              form.save()
              messages.success(request, 'Produto editado com sucesso')
              return redirect('produto')

    return render(request, 'produto/editar_produto.html', {'form':form,'produto_id':produto_id})

def lista_preco(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    produtos = Produto.objects.all().order_by('nome')  # Ordena os produtos por nome
    categorias = Categoria.objects.all().order_by('nome')  # Ordena as categorias por nome
    categoria_id = request.GET.get('categoria')

    if categoria_id:
        categoria_selecionada = Categoria.objects.get(id=categoria_id)
        produtos_categoria = Produto.objects.filter(categoria=categoria_selecionada).order_by('nome')  # Ordena os produtos por nome
    else:
        categoria_selecionada = '0'
        produtos_categoria = Produto.objects.all().order_by('nome')  # Ordena os produtos por nome

    # Agrupar os produtos por subcategoria
    produtos_agrupados = {}
    for produto in produtos_categoria:
        if produto.subcategoria not in produtos_agrupados:
            produtos_agrupados[produto.subcategoria] = []
        produtos_agrupados[produto.subcategoria].append(produto)

    # Ordenar o dicionário de produtos_agrupados pelas chaves (subcategorias)
    produtos_agrupados = dict(sorted(produtos_agrupados.items(), key=lambda x: x[0].nome if x[0] else ''))

    return render(request, 'produto/lista_preco.html', {
        'produtos_agrupados': produtos_agrupados,
        'categorias': categorias,
        'categoria_selecionada': categoria_selecionada,
    })


def cadastro_categoria(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = CategoriaForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('categoria')
        else:
            messages.error(request, 'Erro ao cadastrar o produto. Por favor, verifique os dados informados.')
    else:
        form = CategoriaForms()
    return render(request, 'produto/cadastro_categoria.html', {'form': form})


def cadastro_subcategoria(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = SubcategoriaForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subcategoria cadastrada com sucesso!')
            return redirect('subcategoria')
        else:
            messages.error(request, 'Erro ao cadastrar o produto. Por favor, verifique os dados informados.')
    else:
        form = SubcategoriaForms()
    return render(request, 'produto/cadastro_subcategoria.html', {'form': form})

def lista_categoria(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        categorias = Categoria.objects.all()
        return render(request, 'produto/categoria.html',{"categorias":categorias})

def lista_subcategoria(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        subcategorias = Subcategoria.objects.all()
        return render(request, 'produto/subcategoria.html',{"subcategorias":subcategorias})


def editar_categoria(request, categoria_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    categoria = get_object_or_404(Categoria, id=categoria_id)
    form = CategoriaForms(instance=categoria)

    if request.method == 'POST':
        form = CategoriaForms(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria editada com sucesso')
            return redirect('categoria')

    return render(request, 'produto/editar_categoria.html', {'form': form, 'categoria_id': categoria_id})


def excluir_categoria(request, categoria_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    
    if request.method == 'POST':
        # Verifica se o usuário confirmou a exclusão do pedido
        if 'confirmacao' in request.POST:
            categoria.delete()
            messages.success(request, 'Categoria excluída com sucesso!')
            return redirect(categoria)  
        else:
            messages.error(request, 'Você não confirmou a exclusão.')
            return redirect('categoria')  
        
    return render(request, 'produto/excluir_categoria.html', {'categoria': categoria})

def editar_subcategoria(request, subcategoria_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
    form = SubcategoriaForms(instance=subcategoria)

    if request.method == 'POST':
        form = SubcategoriaForms(request.POST, request.FILES, instance=subcategoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subcategoria editada com sucesso')
            return redirect('subcategoria')

    return render(request, 'produto/editar_subcategoria.html', {'form': form, 'subcategoria_id': subcategoria_id})


def excluir_subcategoria(request, subcategoria_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    subcategoria = get_object_or_404(Subcategoria, pk=subcategoria_id)
    
    if request.method == 'POST':
        # Verifica se o usuário confirmou a exclusão do pedido
        if 'confirmacao' in request.POST:
            subcategoria.delete()
            messages.success(request, 'Subcategoria excluída com sucesso!')
            return redirect(subcategoria)  
        else:
            messages.error(request, 'Você não confirmou a exclusão.')
            return redirect('subcategoria')  
        
    return render(request, 'produto/excluir_subcategoria.html', {'subcategoria': subcategoria})