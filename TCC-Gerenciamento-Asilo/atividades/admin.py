from django.contrib import admin
from .models import RotinaDiaria, HorarioAtividade

@admin.register(RotinaDiaria)
class RotinaAdmin(admin.ModelAdmin):
    list_display = ['idoso', 'data', 'turno', 'responsavel']
    list_filter = ['turno', 'data']

@admin.register(HorarioAtividade)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'horario', 'dias_semana', 'ativo']
    list_filter = ['tipo', 'ativo']
