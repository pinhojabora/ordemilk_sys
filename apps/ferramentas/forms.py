from django import forms

from apps.ferramentas.models import Tensao_energia, Modelo_sala, Modelo_equipamento, Tipo_linha, Tipo_contencao, Tipo_gerenciamento

class Tensao_energiaForms(forms.ModelForm):
        class Meta:
                model = Tensao_energia
                fields = '__all__'
                exclude = []
                labels = {
            'tensao_energia_nome':'Tensão',
        }


        widgets = {
         'tensao_energia_nome': forms.TextInput(attrs={'class':'form-control'}),   
        }


class Modelo_salaForms(forms.ModelForm):
        class Meta:
                model = Modelo_sala
                fields = '__all__'
                exclude = []
                labels = {
            'modelo_sala_nome':'Modelo de sala',
        }


        widgets = {
         'modelo_sala_nome': forms.TextInput(attrs={'class':'form-control'}),   
        }

class Modelo_equipamentoForms(forms.ModelForm):
        class Meta:
                model = Modelo_equipamento
                fields = '__all__'
                exclude = []
                labels = {
            'modelo_equipamento_nome':'Modelo de equipamento',
        }


        widgets = {
         'modelo_sala_nome': forms.TextInput(attrs={'class':'form-control'}),   
        }

class Tipo_linhaForms(forms.ModelForm):
        class Meta:
                model = Tipo_linha
                fields = '__all__'
                exclude = []
                labels = {
            'tipo_linha_nome':'Tipo da linha',
        }


        widgets = {
         'tipo_linha_nome': forms.TextInput(attrs={'class':'form-control'}),   
        }

class Tipo_contencaoForms(forms.ModelForm):
        class Meta:
                model = Tipo_contencao
                fields = '__all__'
                exclude = []
                labels = {
            'tipo_contencao_nome':'Tipo da contencao',
        }


        widgets = {
         'tipo_contencao_nome': forms.TextInput(attrs={'class':'form-control'}),   
        }

class Tipo_gerenciamentoForms(forms.ModelForm):
        class Meta:
                model = Tipo_gerenciamento
                fields = '__all__'
                exclude = []
                labels = {
            'tipo_gerenciamento_nome':'Tipo do gerenciamento',
        }


        widgets = {
         'tipo_gerenciamento_nome': forms.TextInput(attrs={'class':'form-control'}),   
        }