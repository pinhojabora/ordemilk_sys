from django import forms

from apps.pedido.models import Pedido, Parcela_pedido, Item_pedido

class PedidoForms(forms.ModelForm):
        class Meta:
                model = Pedido
                fields = '__all__'
                exclude = ['entrada', 'saldo', 'usuario', 'valor_total']
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
         'parcelas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
         'observacao': forms.Textarea(attrs={'class':'form-control'}),
         
        }

        def save(self, commit=True, user=None):
            instance = super(PedidoForms, self).save(commit=False)
            if user:
                instance.usuario = user
            if commit:
                instance.save()
            return instance
        


class AdicionarParcelaPedidoForm(forms.ModelForm):
    class Meta:
        model = Parcela_pedido
        fields = '__all__'
        exclude = ['pedido','valor_parcela']
 
    widgets = {
            'data_parcela': forms.DateInput(format = '%d/%m/%Y',attrs={'type':'date','class':'form-control'}),
    }         


class ItemPedidoInserirForm(forms.ModelForm):
    class Meta:
        model = Item_pedido
        fields = '__all__'
        exclude = ['pedido','valor_unitario', 'valor_total']

    widgets = {
            'quantidade': forms.TextInput(attrs={'class':'form-control'}),
            'produto': forms.Select(attrs={'class':'form-control'}),
    }

class ItemPedidoEditarForm(forms.ModelForm):
    acrescimo = forms.DecimalField(required=False, label='Acréscimo (%)')
    desconto = forms.DecimalField(required=False, label='Desconto (%)')
    class Meta:
        model = Item_pedido
        fields = '__all__'
        exclude = []
        
    widgets = {
            'quantidade': forms.TextInput(attrs={'class':'form-control'}),
            'produto': forms.Select(attrs={'class':'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
    }