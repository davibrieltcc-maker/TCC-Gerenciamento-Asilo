from django import forms
from .models import SessaoFisioterapia, PlanoReabilitacao


class SessaoForm(forms.ModelForm):
    class Meta:
        model = SessaoFisioterapia
        exclude = ['criado_em']
        widgets = {
            'idoso': forms.Select(attrs={'class': 'form-select'}),
            'fisioterapeuta': forms.Select(attrs={'class': 'form-select'}),
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'objetivo': forms.TextInput(attrs={'class': 'form-control'}),
            'procedimentos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'evolucao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class PlanoForm(forms.ModelForm):
    class Meta:
        model = PlanoReabilitacao
        exclude = ['criado_em']
        widgets = {
            'idoso': forms.Select(attrs={'class': 'form-select'}),
            'fisioterapeuta': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivo_geral': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'exercicios': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'frequencia_semanal': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_previsao_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
