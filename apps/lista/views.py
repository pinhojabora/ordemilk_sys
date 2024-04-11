from django.shortcuts import render, redirect, get_object_or_404

from apps.lista.forms import ListaForms

from django.contrib import messages

from apps.lista.models import Lista


def lista_precos(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        listas = Lista.objects.all()
        return render(request, 'lista/lista_precos.html',{"listas":listas})

def cadastro_lista(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = ListaForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lista de preços cadastrada com sucesso!')
            return redirect('lista_precos')
        else:
            messages.error(request, 'Erro ao cadastrar a lista de preços. Por favor, verifique os dados informados.')
    else:
        form = ListaForms()
    return render(request, 'lista/cadastro_lista.html', {'form': form})

