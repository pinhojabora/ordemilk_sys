from django import forms

from apps.carrinho.models import Carrinho

class CarrinhoForms(forms.ModelForm):
        class Meta:
                model = Carrinho
                fields = '__all__'
                exclude = []
                labels = {
            'quantidade':'Quantidade',
            'valor_unitario': 'Valor Unitário',
            'valor_total': 'Valor Total',         
        }


        widgets = {
         'quantidade': forms.TextInput(attrs={'class':'form-control'}),   
         'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
         'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
          
        }

