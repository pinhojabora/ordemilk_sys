from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.pipeline.forms import PipelineIncludeForms, Fase_pipelineForms, AdicionarEnvolvidoForm, AdicionarItemForm, EditarPropostaForm, EditarPipelineForms, MoverPipelineForm
from apps.pipeline.models import Pipeline, Fase_pipeline, Envolvido_pipeline, Itens_pipeline

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
            pipeline = form.save(commit=False)
            pipeline.usuario = request.user  # Define o usuário atual como o criador do pipeline
            pipeline.save()

            # Após salvar o pipeline, crie um envolvido para o usuário atual
            envolvido = Envolvido_pipeline.objects.create(envolvido=request.user, pipeline=pipeline)

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
    envolvido_pipeline = Envolvido_pipeline.objects.filter(pipeline=prospecto_detalhado)
    item_pipeline = Itens_pipeline.objects.filter(pipeline=prospecto_detalhado)
    return render(request, 'pipeline/detalhes_prospecto.html', {'pipeline': prospecto_detalhado, 'envolvido_pipeline':envolvido_pipeline, 'item_pipeline':item_pipeline})


def editar_prospecto(request, pipeline_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    pipeline = Pipeline.objects.get(id=pipeline_id)
    form = EditarPipelineForms(instance=pipeline)

    if request.method == 'POST':
        form = EditarPipelineForms(request.POST, request.FILES, instance=pipeline)
        if form.is_valid():
            print(request.POST)
            form.save()
            messages.success(request, 'Prospecto editado com sucesso')
            return redirect('detalhes_prospecto',pipeline_id=pipeline_id)

    return render(request, 'pipeline/editar_prospecto.html', {'form': form, 'pipeline_id': pipeline_id})


def quadro_pipeline(request):
    fases = Fase_pipeline.objects.all()
   
    # Filtrar as pipelines em que o usuário atual está envolvido
    pipelines_envolvido = Pipeline.objects.filter(envolvido_pipeline__envolvido=request.user)

    
    pipelines = pipelines_envolvido


    return render(request, 'pipeline/index_pipeline.html', {'fases': fases, 'pipelines': pipelines})



def quadro_geral_pipeline(request):
    fases = Fase_pipeline.objects.all()
   
    # Filtrar as pipelines em que o usuário atual está envolvido
    pipelines_envolvido = Pipeline.objects.all()

    
    pipelines = pipelines_envolvido


    return render(request, 'pipeline/index_geral_pipeline.html', {'fases': fases, 'pipelines': pipelines})



def adicionar_envolvido(request, pipeline_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    pipeline = Pipeline.objects.get(pk=pipeline_id)
    
    if request.method == 'POST':
        form = AdicionarEnvolvidoForm(request.POST)
        if form.is_valid():
            envolvido = form.save(commit=False)
            envolvido.pipeline = pipeline
            envolvido.save()
            return redirect('detalhes_prospecto', pipeline_id=pipeline_id)
    else:
        form = AdicionarEnvolvidoForm()
    
    return render(request, 'pipeline/adicionar_envolvido.html', {'form': form,'pipeline': pipeline})

def excluir_envolvido(request, envolvido_pipeline_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    # Obtenha a parcela existente a ser excluída
    envolvido = get_object_or_404(Envolvido_pipeline, pk=envolvido_pipeline_id)

    if request.method == 'POST':
        # Exclua a parcela
        envolvido.delete()
        return redirect('detalhes_prospecto', pipeline_id=envolvido.pipeline.id)

    return render(request, 'pipeline/excluir_envolvido.html', {'envolvido': envolvido})


def adicionar_item(request, pipeline_id):
    pipeline = Pipeline.objects.get(pk=pipeline_id)

    if request.method == 'POST':
        form = AdicionarItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pipeline = pipeline
            item.save()
            return redirect('detalhes_prospecto', pipeline_id=pipeline_id)
    else:
        form = AdicionarItemForm()

    return render(request, 'pipeline/adicionar_item.html', {'form': form, 'pipeline': pipeline})


def editar_proposta(request, pipeline_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    pipeline = Pipeline.objects.get(id=pipeline_id)
    form = EditarPropostaForm(instance=pipeline)

    if request.method == 'POST':
        form = EditarPropostaForm(request.POST, request.FILES, instance=pipeline)
        if form.is_valid():
            print(request.POST)
            form.save()
            messages.success(request, 'Proposta editada com sucesso')
            return redirect('detalhes_prospecto',pipeline_id=pipeline_id)

    return render(request, 'pipeline/editar_proposta.html', {'form': form, 'pipeline_id': pipeline_id})


def mover_pipeline(request, pipeline_id):
    if not request.user.is_authenticated:
                messages.error(request, 'Usuário não logado')
                return redirect('login')
    
    pipeline = Pipeline.objects.get(id=pipeline_id)
    form = MoverPipelineForm(instance=pipeline)

    if request.method == 'POST':
        form = MoverPipelineForm(request.POST, request.FILES, instance=pipeline)
        if form.is_valid():
            print(request.POST)
            form.save()
            messages.success(request, 'Prospecto movido com sucesso')
            return redirect('index_pipeline')

    return render(request, 'pipeline/mover_pipeline.html', {'form': form, 'pipeline_id': pipeline_id})