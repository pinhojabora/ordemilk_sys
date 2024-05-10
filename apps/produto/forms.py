from django import forms

from apps.produto.models import Produto, Categoria, Subcategoria, Producao1

class ProdutoForms(forms.ModelForm):
        class Meta:
                model = Produto
                fields = '__all__'
                labels = {
            'nome':'Produto',
            'codigo':'Código',
            'unidade':'Unidade',
            'descricao':'Descrição',
            'peso':'Peso',
            'dimensoes': 'Dimensões',
            'preco': 'Preço',
            'preco_com_ipi': 'Preço com IPI',
            'sistema_limpeza': 'Sistema de limpeza',
            'extracao': 'Extração',
            'conj_ordenha': 'Conjunto ordenha',
            'nobreak': 'Nobreak',
        }


        widgets = {
         'nome': forms.TextInput(attrs={}),
         'codigo': forms.TextInput(attrs={'class':'form-control'}),   
         'unidade': forms.TextInput(attrs={'class':'form-control'}),
         'descricao': forms.TextInput(attrs={'class':'form-control'}),
         'peso': forms.TextInput(attrs={'class':'form-control'}),
         'dimensoes': forms.TextInput(attrs={'class':'form-control'}),
         'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
         'preco_com_ipi': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
         'subcategoria': forms.Select(attrs={'class':'form-control'}),
         'sistema_limpeza': forms.CheckboxInput(attrs={}),
         'extracao': forms.CheckboxInput(attrs={}),
         'conj_ordenha': forms.CheckboxInput(attrs={}),
         'nobreak': forms.CheckboxInput(attrs={})
        }

class CategoriaForms(forms.ModelForm):
        class Meta:
                model = Categoria
                fields = '__all__'
                labels = {
            'nome':'Categoria',
        }


        widgets = {
         'nome': forms.TextInput(attrs={}),
         }

class SubcategoriaForms(forms.ModelForm):
        class Meta:
                model = Subcategoria
                fields = '__all__'
                labels = {
            'nome':'Subcategoria',
        }


        widgets = {
         'nome': forms.TextInput(attrs={}),
         }


class ProducaoForms(forms.ModelForm):
        class Meta:
                model = Producao1
                fields = '__all__'
                labels = {
            'codigo':'Código',
            'nome':'Produto',
            'quantidade':'Quantidade',
            
        }


        widgets = {
         'codigo': forms.TextInput(attrs={}),
         'nome': forms.TextInput(attrs={'class':'form-control'}),   
         'quantidade': forms.TextInput(attrs={'class':'form-control'}),
         
        }