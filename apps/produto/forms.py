from django import forms

from apps.produto.models import produto

class ProdutoForms(forms.ModelForm):
        class Meta:
                model = produto
                fields = '__all__'
                labels = {
            'nome':'Produto',
            'codigo':'Código',
            'unidade':'Unidade',
            'descricao':'Descrição',
            'peso':'Peso',
            'dimensoes': 'Dimensões',
            'categoria': 'Categoria',
        }


        widgets = {
         'nome': forms.TextInput(attrs={}),
         'codigo': forms.TextInput(attrs={'class':'form-control'}),   
         'unidade': forms.TextInput(attrs={'class':'form-control'}),
         'descricao': forms.Textarea(attrs={'class':'form-control'}),
         'peso': forms.TextInput(attrs={'class':'form-control'}),
         'dimensoes': forms.TextInput(attrs={'class':'form-control'}),
         'categoria': forms.TextInput(attrs={'class':'form-control'}),
        }

