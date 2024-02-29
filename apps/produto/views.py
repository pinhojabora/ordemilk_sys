from django.shortcuts import render, redirect

from django.contrib import messages

def produto(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        return render(request, 'produto/produto.html')

