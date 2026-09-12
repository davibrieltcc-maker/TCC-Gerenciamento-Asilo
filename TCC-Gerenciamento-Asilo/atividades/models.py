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


DIAS_SEMANA_CHOICES = [
    ('seg', 'Segunda'),
    ('ter', 'Terça'),
    ('qua', 'Quarta'),
    ('qui', 'Quinta'),
    ('sex', 'Sexta'),
    ('sab', 'Sábado'),
    ('dom', 'Domingo'),
]
_CODIGOS_DIAS_SEMANA = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']


class ChecklistAtividade(models.Model):
    """Checklist de atividades personalizadas prescrita para um idoso
    (ex.: caminhada, alongamento), com período e dias da semana em que se aplica."""

    idoso = models.ForeignKey(Idoso, on_delete=models.CASCADE, related_name='checklists_atividades')
    titulo = models.CharField(max_length=150, verbose_name='Título')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    dias_semana = models.CharField(
        max_length=30, verbose_name='Dias da Semana',
        help_text='Códigos separados por vírgula, ex: seg,qua,sex'
    )
    data_inicio = models.DateField(verbose_name='Início')
    data_fim = models.DateField(null=True, blank=True, verbose_name='Fim (deixe em branco para sem prazo)')
    prescrito_por = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, related_name='checklists_prescritas')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Checklist de Atividade'
        verbose_name_plural = 'Checklists de Atividades'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.idoso.nome} – {self.titulo}"

    @property
    def dias_semana_display(self):
        labels = dict(DIAS_SEMANA_CHOICES)
        return ', '.join(labels.get(c, c) for c in self.dias_semana.split(',') if c)

    def aplica_em(self, data):
        """Indica se esta checklist deve ser exibida/registrada na data informada."""
        if not self.ativo or data < self.data_inicio:
            return False
        if self.data_fim and data > self.data_fim:
            return False
        codigo = _CODIGOS_DIAS_SEMANA[data.weekday()]
        return codigo in self.dias_semana.split(',')


class ItemChecklist(models.Model):
    """Uma tarefa dentro de uma checklist de atividades (ex.: 'Caminhada 20 minutos')."""

    checklist = models.ForeignKey(ChecklistAtividade, on_delete=models.CASCADE, related_name='itens')
    descricao = models.CharField(max_length=200, verbose_name='Atividade')
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Item de Checklist'
        verbose_name_plural = 'Itens de Checklist'
        ordering = ['ordem', 'id']

    def __str__(self):
        return self.descricao


class RegistroItemChecklist(models.Model):
    """Execução (ou não) de um item de checklist em um dia específico."""

    item = models.ForeignKey(ItemChecklist, on_delete=models.CASCADE, related_name='registros')
    data = models.DateField()
    realizado = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Registro de Item de Checklist'
        verbose_name_plural = 'Registros de Itens de Checklist'
        ordering = ['-data']
        unique_together = ('item', 'data')

    def __str__(self):
        status = '✓' if self.realizado else '—'
        return f"{status} {self.item.descricao} – {self.data}"


def itens_checklist_do_dia(idoso_id, data):
    """Itens de checklist aplicáveis a um idoso numa data, cada um já anotado
    com `.registro_do_dia` (o RegistroItemChecklist daquele dia, ou None se
    ainda não foi registrado). Não altera nada — apenas consulta.
    """
    checklists = ChecklistAtividade.objects.filter(
        idoso_id=idoso_id, ativo=True).prefetch_related('itens')
    itens = [item for c in checklists if c.aplica_em(data) for item in c.itens.all()]
    registros = {
        r.item_id: r
        for r in RegistroItemChecklist.objects.filter(item__in=itens, data=data)
    }
    for item in itens:
        item.registro_do_dia = registros.get(item.id)
    return itens
