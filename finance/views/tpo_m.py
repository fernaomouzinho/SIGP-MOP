import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from project.models import Project
from payment.models import Invoice
from finance.models import TPO
from finance.forms import TPOForm
from conf.user_utils import c_user_dnof
from conf.utils import getnewid

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofTPOAdd(request, hashid):
    group = request.user.groups.all()[0].name
    dnof = c_user_dnof(request.user)
    inv = get_object_or_404(Invoice, hashed=hashid)
    print(inv)
    
    if request.method == 'POST':
        newid, new_hashid = getnewid(TPO)
        form = TPOForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.proj = inv.cont.project
            instance.cont = inv.cont
            instance.inv = inv
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('tpo-list', hashid=hashid)
    else: form = TPOForm()
    context = {
        'group': group, 'inv': inv, 'form': form,
        'title': 'Aumenta TPO', 'legend': 'Aumenta TPO'
    }
    return render(request, 'finance_tpo/form.html', context)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofTPOEdit(request, hashid, hashid2):
    group = request.user.groups.all()[0].name
    inv = get_object_or_404(Invoice, hashed=hashid)
    objects = get_object_or_404(TPO, hashed=hashid2)
    if request.method == 'POST':
        form = TPOForm(request.POST, instance=objects)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('tpo-list', hashid=hashid)
    else: form = TPOForm(instance=objects)
    context = {
        'group': group,'inv': inv, 'form': form,
        'title': 'Altera TPO', 'legend': 'Altera TPO'
    }
    return render(request, 'finance_tpo/form.html', context)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofTPORem(request, hashid, pk):
    inv = get_object_or_404(Invoice, hashed=hashid)
    tpo = get_object_or_404(TPO, pk=pk)
    tpo.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('tpo-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofTPOReady(request, hashid, pk):
    inv = get_object_or_404(Invoice, hashed=hashid)
    tpo = get_object_or_404(TPO, pk=pk)
    tpo.is_ready = True
    tpo.save()
    messages.success(request, f'Pronto ona.')
    return redirect('tpo-list', hashid=hashid)
