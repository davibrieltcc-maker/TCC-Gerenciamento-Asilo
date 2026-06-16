from django.db import models
from idosos.models import Idoso
from core.models import Usuario


class RotinaDiaria(models.Model):
    """Registro de higienização e alimentação de cada idoso por turno."""
    TURNO_CHOICES = [
        ('manha', 'Manhã (06h–12h)'),
        ('tarde', 'Tarde (12h–18h)'),
        ('noite', 'Noite (18h–06h)'),
    ]
    REFEICAO_CHOICES = [
        ('cafe', 'Café da manhã'),
        ('lanche_manha', 'Lanche da manhã'),
        ('almoco', 'Almoço'),
        ('lanche_tarde', 'Lanche da tarde'),
        ('jantar', 'Jantar'),
        ('ceia', 'Ceia'),
    ]

    idoso = models.ForeignKey(Idoso, on_delete=models.CASCADE, related_name='rotinas')
    data = models.DateField(verbose_name='Data')
    turno = models.CharField(max_length=6, choices=TURNO_CHOICES)
    responsavel = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='rotinas_registradas')

    # Higienização
    banho_realizado = models.BooleanField(default=False, verbose_name='Banho Realizado')
    higiene_oral = models.BooleanField(default=False, verbose_name='Higiene Oral')
    troca_roupa = models.BooleanField(default=False, verbose_name='Troca de Roupa')
    curativo = models.BooleanField(default=False, verbose_name='Curativo Realizado')
    obs_higiene = models.TextField(blank=True, verbose_name='Obs. Higienização')

    # Alimentação
    refeicoes_realizadas = models.CharField(max_length=200, blank=True, verbose_name='Refeições Realizadas')
    aceitacao_alimentar = models.CharField(
        max_length=10,
        choices=[('total', 'Total'), ('parcial', 'Parcial'), ('recusou', 'Recusou')],
        blank=True,
        verbose_name='Aceitação Alimentar'
    )
    obs_alimentacao = models.TextField(blank=True, verbose_name='Obs. Alimentação')

    observacoes_gerais = models.TextField(blank=True, verbose_name='Observações Gerais')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Rotina Diária'
        verbose_name_plural = 'Rotinas Diárias'
        ordering = ['-data', 'turno']
        unique_together = ('idoso', 'data', 'turno')

    def __str__(self):
        return f"{self.idoso.nome} – {self.data} – {self.get_turno_display()}"


class HorarioAtividade(models.Model):
    """Horários fixos de atividades programadas para o asilo."""
    TIPO_CHOICES = [
        ('higiene', 'Higienização'),
        ('alimentacao', 'Alimentação'),
        ('medicamento', 'Medicamento'),
        ('fisioterapia', 'Fisioterapia'),
        ('lazer', 'Atividade de Lazer'),
        ('outro', 'Outro'),
    ]

    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    horario = models.TimeField(verbose_name='Horário')
    dias_semana = models.CharField(max_length=50, help_text='Ex: seg,ter,qua,qui,sex ou todos')
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Horário de Atividade'
        verbose_name_plural = 'Horários de Atividades'
        ordering = ['horario']

    def __str__(self):
        return f"{self.titulo} – {self.horario:%H:%M}"
