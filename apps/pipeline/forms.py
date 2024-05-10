from django import forms
from apps.pipeline.models import Pipeline, Fase_pipeline

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

