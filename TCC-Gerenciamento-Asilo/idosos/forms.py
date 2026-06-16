from django import forms
from .models import Idoso, FamiliarVinculo


class IdosoForm(forms.ModelForm):
    class Meta:
        model = Idoso
        exclude = ['criado_em', 'atualizado_em']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'tipo_sanguineo': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'numero_quarto': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'condicoes_medicas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class FamiliarVinculoForm(forms.ModelForm):
    class Meta:
        model = FamiliarVinculo
        fields = ['familiar', 'parentesco', 'contato_principal']
        widgets = {
            'familiar': forms.Select(attrs={'class': 'form-select'}),
            'parentesco': forms.TextInput(attrs={'class': 'form-control'}),
            'contato_principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
