from django import forms
from .models import RotinaDiaria


class RotinaForm(forms.ModelForm):
    class Meta:
        model = RotinaDiaria
        exclude = ['responsavel', 'criado_em']
        widgets = {
            'idoso': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-select'}),
            'banho_realizado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'higiene_oral': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'troca_roupa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'curativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'obs_higiene': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'refeicoes_realizadas': forms.TextInput(attrs={'class': 'form-control'}),
            'aceitacao_alimentar': forms.Select(attrs={'class': 'form-select'}),
            'obs_alimentacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observacoes_gerais': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
