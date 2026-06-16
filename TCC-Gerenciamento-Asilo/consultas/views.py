from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Consulta, Prontuario
from .forms import ConsultaForm, ProntuarioForm
from core.decorators import perfil_required, saude_required


@login_required
@saude_required
def lista(request):
    consultas = Consulta.objects.select_related('idoso', 'medico').order_by('-data_hora')[:50]
    return render(request, 'consultas/lista.html', {'consultas': consultas})

@login_required
@saude_required
def detalhe(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    return render(request, 'consultas/detalhe.html', {'consulta': consulta})

@login_required
@perfil_required('administrador', 'medico', 'recepcionista')
def novo(request):
    form = ConsultaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Consulta agendada!')
        return redirect('consultas:lista')
    return render(request, 'consultas/form.html', {'form': form, 'titulo': 'Nova Consulta'})

@login_required
@perfil_required('administrador', 'medico')
def editar(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    form = ConsultaForm(request.POST or None, instance=consulta)
    if form.is_valid():
        form.save()
        messages.success(request, 'Consulta atualizada!')
        return redirect('consultas:lista')
    return render(request, 'consultas/form.html', {'form': form, 'titulo': 'Editar Consulta'})

@login_required
@perfil_required('administrador')
def excluir(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        consulta.delete()
        return redirect('consultas:lista')
    return render(request, 'consultas/confirmar_exclusao.html', {'consulta': consulta})
