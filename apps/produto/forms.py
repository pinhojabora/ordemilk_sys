from django import forms
class ProdutoForms(forms.Form):
        nome=forms.CharField(
        label='Nome do Produto', 
        required=True, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Produto',
            }
        )
    )
        codigo=forms.CharField(
        label='Código',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 99999',
            }
        )
    )
        unidade=forms.CharField(
        label='Unidade', 
        required=True, 
        max_length=4,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: UN',
            }
        ),
    )
