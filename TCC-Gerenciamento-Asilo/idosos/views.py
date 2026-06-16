from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Idoso, FamiliarVinculo
from .forms import IdosoForm, FamiliarVinculoForm
from core.decorators import perfil_required, admin_ou_recepcionista_required


@login_required
def lista(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', 'ativo')
    idosos = Idoso.objects.all()

    # Familiar vê apenas seus vinculados
    if request.user.is_familiar:
        vinculos = FamiliarVinculo.objects.filter(
            familiar=request.user).values_list('idoso_id', flat=True)
        idosos = idosos.filter(id__in=vinculos)

    if q:
        idosos = idosos.filter(Q(nome__icontains=q) | Q(cpf__icontains=q))
    if status:
        idosos = idosos.filter(status=status)

    return render(request, 'idosos/lista.html', {
        'idosos': idosos, 'q': q, 'status_filtro': status
    })


@login_required
def detalhe(request, pk):
    idoso = get_object_or_404(Idoso, pk=pk)
    # Familiar: verifica vínculo
    if request.user.is_familiar:
        if not FamiliarVinculo.objects.filter(
                familiar=request.user, idoso=idoso).exists():
            messages.error(request, 'Acesso negado.')
            return redirect('idosos:lista')
    return render(request, 'idosos/detalhe.html', {'idoso': idoso})


@login_required
@admin_ou_recepcionista_required   # RN: só admin e recepcionista cadastram idosos
def novo(request):
    form = IdosoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Idoso cadastrado com sucesso!')
        return redirect('idosos:lista')
    return render(request, 'idosos/form.html', {'form': form, 'titulo': 'Novo Idoso'})


@login_required
@admin_ou_recepcionista_required
def editar(request, pk):
    idoso = get_object_or_404(Idoso, pk=pk)
    form = IdosoForm(request.POST or None, request.FILES or None, instance=idoso)
    if form.is_valid():
        form.save()
        messages.success(request, 'Idoso atualizado com sucesso!')
        return redirect('idosos:detalhe', pk=pk)
    return render(request, 'idosos/form.html', {
        'form': form, 'titulo': 'Editar Idoso', 'idoso': idoso
    })


@login_required
@perfil_required('administrador')
def excluir(request, pk):
    idoso = get_object_or_404(Idoso, pk=pk)
    if request.method == 'POST':
        idoso.delete()
        messages.success(request, 'Idoso removido.')
        return redirect('idosos:lista')
    return render(request, 'idosos/confirmar_exclusao.html', {'idoso': idoso})


@login_required
@admin_ou_recepcionista_required
def vincular_familiar(request, idoso_pk):
    """Vincula um familiar a um idoso."""
    idoso = get_object_or_404(Idoso, pk=idoso_pk)
    form = FamiliarVinculoForm(request.POST or None)
    if form.is_valid():
        v = form.save(commit=False)
        v.idoso = idoso
        v.save()
        messages.success(request, 'Familiar vinculado!')
        return redirect('idosos:detalhe', pk=idoso_pk)
    return render(request, 'idosos/vincular_familiar.html', {
        'form': form, 'idoso': idoso
    })
