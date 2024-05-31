from django import forms
from apps.pipeline.models import Pipeline, Fase_pipeline, Envolvido_pipeline, Itens_pipeline

class PipelineIncludeForms(forms.ModelForm):
        class Meta:
                model = Pipeline
                fields = '__all__'
                exclude = ['produto_customizado', 'detalhes_proposta', 'total_proposta','desconto_proposta', 'acrescimo_proposta', 'final_proposta', 'validade_proposta', 'usuario', 'situacao', 'fase', 'demo_tecnica']
                labels = {
            'data_inclusao':'Data',
            'titulo':'Titulo da negociacao',
            'cliente':'Cliente',
            'pessoa_contato':'Contato',
            'telefone':'Telefone',
            'email':'E-mail',
            'cidade':'Cidade',
            'estado':'Estado',
            'setor_atividade':'Setor ou Atividade',
            'fonte_lead':'Fonte do Lead',
            'detalhes_oportunidade':'Detalhes da Oportunidade',
                        
        }


        widgets = {
         'data_inclusao': forms.DateInput(
        format = '%d/%m/%Y',
        attrs={
            'type':'date',
            'class':'form-control'
            }
        ),
         'titulo': forms.TextInput(attrs={'class':'form-control'}),   
         'cliente': forms.TextInput(attrs={'class':'form-control'}),
         'pessoa_contato': forms.TextInput(attrs={'class':'form-control'}),
         'telefone': forms.TextInput(attrs={'class':'form-control'}),
         'email': forms.TextInput(attrs={'class':'form-control'}),
         'cidade': forms.TextInput(attrs={'class':'form-control'}),
         'estado': forms.TextInput(attrs={'class':'form-control'}),
         'setor_atividade': forms.TextInput(attrs={'class':'form-control'}),
         'fonte_lead': forms.TextInput(attrs={'class':'form-control'}),
         'detalhes_oportunidade': forms.Textarea(attrs={'class':'form-control'}),
                           
        }

        def save(self, commit=True, user=None):
            instance = super(PipelineIncludeForms, self).save(commit=False)
            if user:
                instance.usuario = user
            if commit:
                instance.save()
            return instance
        

class Fase_pipelineForms(forms.ModelForm):
        class Meta:
                model = Fase_pipeline
                fields = '__all__'
                exclude = []
                labels = {
            'nome_fase':'Fase',
        }


        widgets = {
         'nome_fase': forms.TextInput(attrs={'class':'form-control'}),   
        }


class AdicionarEnvolvidoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.pipeline = kwargs.pop('pipeline', None)
        super().__init__(*args, **kwargs)
        if self.pipeline:
            self.fields['envolvido'].queryset = self.pipeline.envolvidos.all()

        # Personalize o widget do campo envolvido para exibir o nome completo
        self.fields['envolvido'].widget = forms.Select(choices=self.envolvido_choices())

    def envolvido_choices(self):
        # Gere as opções para o campo envolvido com o nome completo
        choices = [(envolvido.id, envolvido.get_full_name()) for envolvido in self.fields['envolvido'].queryset]
        return choices

    class Meta:
        model = Envolvido_pipeline
        fields = ['envolvido']


class AdicionarItemForm(forms.ModelForm):
    class Meta:
        model = Itens_pipeline
        fields = ['produto', 'quantidade']


class EditarPropostaForm(forms.ModelForm):
    class Meta:
        model = Pipeline
        fields = ['detalhes_proposta', 'total_proposta','desconto_proposta','acrescimo_proposta','final_proposta','validade_proposta']


class EditarPipelineForms(forms.ModelForm):
        class Meta:
                model = Pipeline
                fields = '__all__'
                exclude = ['detalhes_proposta', 'total_proposta','desconto_proposta', 'acrescimo_proposta', 'final_proposta', 'validade_proposta', 'usuario', 'situacao', 'fase']
                labels = {
            'data_inclusao':'Data',
            'titulo':'Titulo da negociacao',
            'cliente':'Cliente',
            'pessoa_contato':'Contato',
            'telefone':'Telefone',
            'email':'E-mail',
            'cidade':'Cidade',
            'estado':'Estado',
            'setor_atividade':'Setor ou Atividade',
            'fonte_lead':'Fonte do Lead',
            'detalhes_oportunidade':'Detalhes da Oportunidade',
            'produto_customizado' : 'Produto Customizado',
            'demo_tecnica' : 'Demonstração Técnica',

                        
        }


        widgets = {
         'data_inclusao': forms.DateInput(
        format = '%d/%m/%Y',
        attrs={
            'type':'date',
            'class':'form-control'
            }
        ),
         'titulo': forms.TextInput(attrs={'class':'form-control'}),   
         'cliente': forms.TextInput(attrs={'class':'form-control'}),
         'pessoa_contato': forms.TextInput(attrs={'class':'form-control'}),
         'telefone': forms.TextInput(attrs={'class':'form-control'}),
         'email': forms.TextInput(attrs={'class':'form-control'}),
         'cidade': forms.TextInput(attrs={'class':'form-control'}),
         'estado': forms.TextInput(attrs={'class':'form-control'}),
         'setor_atividade': forms.TextInput(attrs={'class':'form-control'}),
         'fonte_lead': forms.TextInput(attrs={'class':'form-control'}),
         'detalhes_oportunidade': forms.Textarea(attrs={'class':'form-control'}),
         'produto_customizado': forms.Textarea(attrs={'class':'form-control'}),
         'demo_tecnica' : forms.CheckboxInput(attrs={}),                  
        }


class MoverPipelineForm(forms.ModelForm):
    class Meta:
        model = Pipeline
        fields = ['fase']