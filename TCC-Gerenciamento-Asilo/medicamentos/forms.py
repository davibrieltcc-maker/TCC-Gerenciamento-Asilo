from django import forms
from .models import Medicamento, PrescricaoMedicamento, RegistroAdministracao


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        exclude = ['criado_em', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'principio_ativo': forms.TextInput(attrs={'class': 'form-control'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control'}),
            'forma': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: comprimido, xarope'}),
            'estoque_atual': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidade': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PrescricaoForm(forms.ModelForm):
    class Meta:
        model = PrescricaoMedicamento
        exclude = ['idoso', 'prescrito_por', 'criado_em']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-select'}),
            'dose': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 500mg'}),
            'frequencia': forms.Select(attrs={'class': 'form-select'}),
            'horarios': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 08:00, 14:00, 20:00'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'via_administracao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: oral'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AdministracaoForm(forms.ModelForm):
    class Meta:
        model = RegistroAdministracao
        exclude = ['prescricao', 'administrado_por', 'criado_em']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
