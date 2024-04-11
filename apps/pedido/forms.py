from django import forms

from apps.pedido.models import Pedido

class PedidoForms(forms.ModelForm):
        class Meta:
                model = Pedido
                fields = '__all__'
                exclude = ['entrada', 'saldo']
                labels = {
            'data_pedido':'Data',
            'nome_cliente':'Cliente',
            'endereco_cliente':'Endereço',
            'cidade':'Cidade',
            'estado':'Estado',
            'cep': 'CEP',
            'cnpj_cpf': 'CNPJ/CPF',
            'insc_estadual': 'Inscrição Estadual',
            'fone': 'Fone',
            'email': 'E-mail',
            'forma_pagamento': 'Forma de pagamento',
            'pagamento': 'Pagamento em',
            'valor_total': 'Valor total',
            'parcelas': 'Parcelas',
            'observacao': 'Observações',

        }


        widgets = {
         'data_pedido': forms.DateInput(
        format = '%d/%m/%Y',
        attrs={
            'type':'date',
            'class':'form-control'
            }
        ),
         'nome_cliente': forms.TextInput(attrs={'class':'form-control'}),   
         'endereco_cliente': forms.TextInput(attrs={'class':'form-control'}),
         'cidade': forms.TextInput(attrs={'class':'form-control'}),
         'estado': forms.TextInput(attrs={'class':'form-control'}),
         'cep': forms.TextInput(attrs={'class':'form-control'}),
         'cnpj_cpf': forms.TextInput(attrs={'class':'form-control'}),
         'insc_estadual': forms.TextInput(attrs={'class':'form-control'}),
         'fone': forms.TextInput(attrs={'class':'form-control'}),
         'email': forms.TextInput(attrs={'class':'form-control'}),
         'forma_pagamento': forms.Select(attrs={'class':'form-control'}),
         'pagamento': forms.Select(attrs={'class':'form-control'}),
         'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
         'parcelas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
         'observacao': forms.Textarea(attrs={'class':'form-control'}),
 
        }

