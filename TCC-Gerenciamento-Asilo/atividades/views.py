from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import date, datetime
from .models import (
    RotinaDiaria, HorarioAtividade, ChecklistAtividade, ItemChecklist,
    RegistroItemChecklist, itens_checklist_do_dia,
)
from .forms import RotinaForm, ChecklistAtividadeForm, ItemChecklistFormSet
from core.decorators import perfil_required


ORDENACOES = {
    'recentes': ('-data', 'turno', 'idoso__nome'),
    'antigas': ('data', 'turno', 'idoso__nome'),
    'nome_asc': ('idoso__nome', '-data', 'turno'),
    'nome_desc': ('-idoso__nome', '-data', 'turno'),
}


def _anexar_resumo_checklist(rotinas):
    """Anota cada rotina com `.checklist_resumo`: os itens de checklist do
    idoso aplicáveis naquele dia, com o status de execução (ou pendente)."""
    rotinas = list(rotinas)
    cache = {}
    for r in rotinas:
        chave = (r.idoso_id, r.data)
        if chave not in cache:
            cache[chave] = itens_checklist_do_dia(r.idoso_id, r.data)
        r.checklist_resumo = cache[chave]
    return rotinas


@login_required
def lista(request):
    user = request.user
    data_param = request.GET.get('data', '').strip()
    idoso_param = request.GET.get('idoso', '').strip()
    turno_param = request.GET.get('turno', '').strip()
    ordenar_param = request.GET.get('ordenar', 'recentes').strip()
    if ordenar_param not in ORDENACOES:
        ordenar_param = 'recentes'

    # Valida a data se foi informada
    data_valida = None
    if data_param:
        try:
            datetime.strptime(data_param, '%Y-%m-%d')
            data_valida = data_param
        except ValueError:
            data_valida = None

    if user.is_familiar:
        from idosos.models import FamiliarVinculo, Idoso
        idosos_ids = list(FamiliarVinculo.objects.filter(
            familiar=user).values_list('idoso_id', flat=True))
        rotinas = RotinaDiaria.objects.filter(idoso__in=idosos_ids)
        idosos_filtro = Idoso.objects.filter(id__in=idosos_ids).order_by('nome')
        horarios = []
    else:
        rotinas = RotinaDiaria.objects.all()
        from idosos.models import Idoso
        idosos_filtro = Idoso.objects.order_by('nome')
        horarios = HorarioAtividade.objects.filter(ativo=True).order_by('horario')

    rotinas = rotinas.select_related('idoso', 'responsavel')
    if data_valida:
        rotinas = rotinas.filter(data=data_valida)
    if idoso_param.isdigit():
        rotinas = rotinas.filter(idoso_id=idoso_param)
    if turno_param in dict(RotinaDiaria.TURNO_CHOICES):
        rotinas = rotinas.filter(turno=turno_param)
    rotinas = rotinas.order_by(*ORDENACOES[ordenar_param])

    return render(request, 'atividades/lista.html', {
        'rotinas': _anexar_resumo_checklist(rotinas),
        'data_filtro': data_valida or '',
        'idoso_filtro': idoso_param,
        'turno_filtro': turno_param,
        'ordenar_filtro': ordenar_param,
        'idosos_filtro': idosos_filtro,
        'turno_choices': RotinaDiaria.TURNO_CHOICES,
        'horarios': horarios,
    })


@login_required
def detalhe(request, pk):
    rotina = get_object_or_404(RotinaDiaria, pk=pk)
    checklist_itens = itens_checklist_do_dia(rotina.idoso_id, rotina.data)
    return render(request, 'atividades/detalhe.html', {
        'rotina': rotina, 'checklist_itens': checklist_itens,
    })


def _salvar_registros_checklist(request, rotina):
    """Grava/atualiza a execução dos itens de checklist marcados na tela de Rotina.

    Os ids dos itens exibidos vêm num campo oculto ('checklist_item_ids'),
    já que checkboxes desmarcados simplesmente não aparecem no POST.
    """
    ids = [i for i in request.POST.get('checklist_item_ids', '').split(',') if i]
    for id_str in ids:
        item = ItemChecklist.objects.filter(pk=id_str, checklist__idoso=rotina.idoso).first()
        if not item:
            continue
        RegistroItemChecklist.objects.update_or_create(
            item=item, data=rotina.data,
            defaults={
                'realizado': request.POST.get(f'item_realizado_{id_str}') == 'on',
                'observacoes': request.POST.get(f'item_obs_{id_str}', '').strip(),
                'registrado_por': request.user,
            }
        )


@login_required
@perfil_required('administrador', 'enfermeiro', 'recepcionista')
def novo(request):
    form = RotinaForm(request.POST or None)
    if form.is_valid():
        r = form.save(commit=False)
        r.responsavel = request.user
        r.save()
        _salvar_registros_checklist(request, r)
        messages.success(request, 'Rotina registrada!')
        return redirect('atividades:lista')
    return render(request, 'atividades/form.html', {
        'form': form, 'titulo': 'Registrar Rotina'
    })


@login_required
@perfil_required('administrador', 'enfermeiro')
def editar(request, pk):
    rotina = get_object_or_404(RotinaDiaria, pk=pk)
    form = RotinaForm(request.POST or None, instance=rotina)
    if form.is_valid():
        form.save()
        _salvar_registros_checklist(request, rotina)
        messages.success(request, 'Rotina atualizada!')
        return redirect('atividades:lista')
    return render(request, 'atividades/form.html', {
        'form': form, 'titulo': 'Editar Rotina'
    })


@login_required
def atividades_do_dia(request):
    """Endpoint AJAX: itens de checklist aplicáveis a um idoso numa data,
    já indicando se há registro de execução salvo para aquele dia."""
    idoso_id = request.GET.get('idoso')
    data_param = request.GET.get('data')
    if not idoso_id or not data_param:
        return JsonResponse({'items': []})
    try:
        data_ref = datetime.strptime(data_param, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'items': []})

    itens = itens_checklist_do_dia(idoso_id, data_ref)
    items = [{
        'id': item.id,
        'descricao': item.descricao,
        'checklist_titulo': item.checklist.titulo,
        'realizado': item.registro_do_dia.realizado if item.registro_do_dia else False,
        'observacoes': item.registro_do_dia.observacoes if item.registro_do_dia else '',
    } for item in itens]
    return JsonResponse({'items': items})


@login_required
@perfil_required('administrador', 'medico', 'enfermeiro', 'fisioterapeuta')
def checklist_lista(request, idoso_pk):
    from idosos.models import Idoso
    idoso = get_object_or_404(Idoso, pk=idoso_pk)
    checklists = idoso.checklists_atividades.prefetch_related('itens').order_by('-ativo', '-criado_em')
    return render(request, 'atividades/checklist_lista.html', {
        'idoso': idoso, 'checklists': checklists,
    })


@login_required
@perfil_required('administrador', 'medico', 'enfermeiro', 'fisioterapeuta')
def checklist_novo(request, idoso_pk):
    from idosos.models import Idoso
    idoso = get_object_or_404(Idoso, pk=idoso_pk)
    form = ChecklistAtividadeForm(request.POST or None)
    formset = ItemChecklistFormSet(request.POST or None, instance=ChecklistAtividade())
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        obj = form.save(commit=False)
        obj.idoso = idoso
        obj.prescrito_por = request.user
        obj.save()
        formset.instance = obj
        formset.save()
        messages.success(request, 'Checklist de atividades criada!')
        return redirect('idosos:detalhe', pk=idoso_pk)
    return render(request, 'atividades/checklist_form.html', {
        'form': form, 'formset': formset, 'idoso': idoso, 'titulo': 'Nova Checklist de Atividades'
    })


@login_required
@perfil_required('administrador', 'medico', 'enfermeiro', 'fisioterapeuta')
def checklist_editar(request, pk):
    checklist = get_object_or_404(ChecklistAtividade, pk=pk)
    form = ChecklistAtividadeForm(request.POST or None, instance=checklist)
    formset = ItemChecklistFormSet(request.POST or None, instance=checklist)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        messages.success(request, 'Checklist atualizada!')
        return redirect('idosos:detalhe', pk=checklist.idoso_id)
    return render(request, 'atividades/checklist_form.html', {
        'form': form, 'formset': formset, 'idoso': checklist.idoso,
        'checklist': checklist, 'titulo': 'Editar Checklist de Atividades'
    })


@login_required
@perfil_required('administrador', 'medico', 'enfermeiro', 'fisioterapeuta')
def checklist_encerrar(request, pk):
    checklist = get_object_or_404(ChecklistAtividade, pk=pk)
    if request.method == 'POST':
        checklist.ativo = False
        checklist.save(update_fields=['ativo'])
        messages.success(request, 'Checklist encerrada.')
        return redirect('idosos:detalhe', pk=checklist.idoso_id)
    return render(request, 'atividades/confirmar_encerrar_checklist.html', {'checklist': checklist})


@login_required
@perfil_required('administrador')
def excluir(request, pk):
    rotina = get_object_or_404(RotinaDiaria, pk=pk)
    if request.method == 'POST':
        rotina.delete()
        return redirect('atividades:lista')
    return render(request, 'atividades/confirmar_exclusao.html', {'rotina': rotina})