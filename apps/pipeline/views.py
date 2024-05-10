from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.pipeline.forms import PipelineIncludeForms, Fase_pipelineForms
from apps.pipeline.models import Pipeline, Fase_pipeline

def index_pipeline(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
        
        return render(request, 'pipeline/index_pipeline.html')

def lista_pipeline(request):
        if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')

        pipelines = Pipeline.objects.all()
        return render(request, 'pipeline/pipeline.html',{"pipelines":pipelines})


def cadastro_prospecto(request):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    if request.method == 'POST':
        form = PipelineIncludeForms(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Prospecto cadastrado com sucesso!')
            return redirect('index_pipeline')
        else:
            messages.error(request, 'Erro ao cadastrar o prospecto. Por favor, verifique os dados informados.')
    else:
        form = PipelineIncludeForms()
    return render(request, 'pipeline/cadastro_prospecto.html', {'form': form})


def detalhes_prospecto(request, pipeline_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    prospecto_detalhado = Pipeline.objects.get(pk=pipeline_id)
    return render(request, 'pipeline/detalhes_prospecto.html', {'pipeline': prospecto_detalhado})


def quadro_pipeline(request):
    fases = Fase_pipeline.objects.all()
    pipelines = Pipeline.objects.all()

    return render(request, 'pipeline/index_pipeline.html', {'fases': fases, 'pipelines': pipelines})

