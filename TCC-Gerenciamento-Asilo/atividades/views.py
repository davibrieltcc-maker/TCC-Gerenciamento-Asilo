from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from .models import RotinaDiaria, HorarioAtividade
from .forms import RotinaForm
from core.decorators import perfil_required


@login_required
def lista(request):
    user = request.user
    data = request.GET.get('data', str(date.today()))

    if user.is_familiar:
        from idosos.models import FamiliarVinculo
        idosos_ids = FamiliarVinculo.objects.filter(familiar=user).values_list('idoso_id', flat=True)
        rotinas = RotinaDiaria.objects.filter(
            data=data, idoso__in=idosos_ids
        ).select_related('idoso', 'responsavel').order_by('turno')
        return render(request, 'atividades/lista.html', {'rotinas': rotinas, 'data_filtro': data, 'horarios': []})

    rotinas = RotinaDiaria.objects.filter(data=data).select_related('idoso', 'responsavel').order_by('turno')
    horarios = HorarioAtividade.objects.filter(ativo=True).order_by('horario')
    return render(request, 'atividades/lista.html', {'rotinas': rotinas, 'data_filtro': data, 'horarios': horarios})

@login_required
def detalhe(request, pk):
    rotina = get_object_or_404(RotinaDiaria, pk=pk)
    return render(request, 'atividades/detalhe.html', {'rotina': rotina})

@login_required
@perfil_required('administrador', 'enfermeiro', 'recepcionista')
def novo(request):
    form = RotinaForm(request.POST or None)
    if form.is_valid():
        r = form.save(commit=False)
        r.responsavel = request.user
        r.save()
        messages.success(request, 'Rotina registrada!')
        return redirect('atividades:lista')
    return render(request, 'atividades/form.html', {'form': form, 'titulo': 'Registrar Rotina'})

@login_required
@perfil_required('administrador', 'enfermeiro')
def editar(request, pk):
    rotina = get_object_or_404(RotinaDiaria, pk=pk)
    form = RotinaForm(request.POST or None, instance=rotina)
    if form.is_valid():
        form.save()
        messages.success(request, 'Rotina atualizada!')
        return redirect('atividades:lista')
    return render(request, 'atividades/form.html', {'form': form, 'titulo': 'Editar Rotina'})

@login_required
@perfil_required('administrador')
def excluir(request, pk):
    rotina = get_object_or_404(RotinaDiaria, pk=pk)
    if request.method == 'POST':
        rotina.delete()
        return redirect('atividades:lista')
    return render(request, 'atividades/confirmar_exclusao.html', {'rotina': rotina})
