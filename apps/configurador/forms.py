from django import forms

from apps.configurador.models import Configurador

class ConfiguradorForms(forms.ModelForm):
        class Meta:
                model = Configurador
                fields = '__all__'
                exclude = ['usuario', 'vacuo_recomendado', 'valor_total', 'gerenciamento','quant_gerenciamento', 'numero_conjuntos', 'fator_calculo_modelo', 'tipo_gerenciamento']
                labels = {
            'data_configurador':'Data',
            'nome_cliente':'Cliente',
            'nome_fazenda':'Nome da fazenda',
            'cidade':'Cidade',
            'estado':'Estado',
            'altitude':'Altitude',
            'fone': 'Fone',
            

        }


        widgets = {
         'data_configurador': forms.DateInput(
        format = '%d/%m/%Y',
        attrs={
            'type':'date',
            'class':'form-control'
            }
        ),
         'nome_cliente': forms.TextInput(attrs={'class':'form-control'}),   
         'nome_fazenda': forms.TextInput(attrs={'class':'form-control'}),
         'cidade': forms.TextInput(attrs={'class':'form-control'}),
         'estado': forms.TextInput(attrs={'class':'form-control'}),
         'cep': forms.TextInput(attrs={'class':'form-control'}),
         'altitude': forms.NumberInput(attrs={'class':'form-control'}),
         'fone': forms.TextInput(attrs={'class':'form-control'}),
        
 
        }
        def save(self, commit=True, user=None):
            instance = super(ConfiguradorForms, self).save(commit=False)
            if user:
                instance.usuario = user
            if commit:
                instance.save()
            return instance
class ItemConfiguradorForm(forms.Form):
    configurador_id = forms.IntegerField(widget=forms.HiddenInput())
    produto_id = forms.IntegerField(widget=forms.HiddenInput())


class AtivaGerenciamentoForm(forms.ModelForm):
        class Meta:
               model = Configurador
               fields = ['gerenciamento']
        widgets = {
            
           'gerenciamento': forms.CheckboxInput(attrs={}),
        }

class SelecionaGerenciamentoForm(forms.ModelForm):
        class Meta:
               model = Configurador
               fields = ['tipo_gerenciamento', 'quant_gerenciamento']
        widgets = {
            
           'quant_gerenciamento': forms.TextInput(attrs={}),
        }

