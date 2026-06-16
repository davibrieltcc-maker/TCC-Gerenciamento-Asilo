from django import forms
from .models import Funcionario


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        exclude = ['criado_em']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'registro_profissional': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidade': forms.TextInput(attrs={'class': 'form-control'}),
            'vinculo': forms.Select(attrs={'class': 'form-select'}),
            'data_admissao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_demissao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control'}),
            'turno': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
