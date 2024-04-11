from django import forms

from apps.lista.models import Lista

from apps.produto.models import Produto

class ListaForms(forms.ModelForm):
        class Meta:
                model = Lista
                fields = '__all__'
                labels = {
            'nome_lista':'Lista',
            'periodo':'Período',
            'vigencia':'Vigência',
            'data_lista':'Data da lista',
            'observacao': 'Observação',
            'ativa': 'Ativa',
        }


        widgets = {
         'nome_lista': forms.TextInput(attrs={}),
         'periodo': forms.TextInput(attrs={'class':'form-control'}),   
         'vigencia': forms.TextInput(attrs={'class':'form-control'}),
         'data_lista': forms.DateTimeInput(attrs={'class':'form-control'}),
         'observacao': forms.Textarea(attrs={'class':'form-control'}),
         'ativa': forms.CheckboxInput(attrs={'class':'form--check-input'}),
        }


