import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Sum, Count, Q
from django.contrib import messages
from contract.models import Contract, ContractComp
from invoice.models import Invoice, PayRecom
from invoice.forms import PayRecomForm
from conf.utils import getnewid
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipRecomDet(request, hashid):
    group = get_roles(request)
    recom = get_object_or_404(PayRecom, hashed=hashid)   
    inv = recom.inv
    contcomp = ContractComp.objects.filter(contract=inv.cont).first()
    context = {
        'group': group, 'inv': inv, 'cont': inv.cont, 'recom':recom,'contcomp':contcomp,
        'title': 'Rekomendasaun Pagamentu', 'legend': 'Rekomendasaun Pagamentu'
    }
    return render(request, 'inv_recom/detail.html', context)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipRecomAdd(request, hashid):
    inv = get_object_or_404(Invoice, hashed=hashid)
    if request.method == 'POST':
        newid, new_hashid = getnewid(PayRecom)
        form = PayRecomForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.cont = inv.cont
            instance.inv = inv
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('uvip-recom-det', hashid=new_hashid)
    else: form = PayRecomForm()
    context = {
        'inv': inv, 'form': form,
        'title': 'Aumenta Rekomendasaun Pagamentu', 'legend': 'Aumenta Rekomendasaun Pagamentu'
    }
    return render(request, 'inv_recom/form.html', context)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipRecomEdit(request, hashid):
    obj = get_object_or_404(PayRecom, hashed=hashid)
    inv = obj.inv
    if request.method == 'POST':
        form = PayRecomForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('uvip-recom-det', hashid=hashid)
    else: form = PayRecomForm(instance=obj)
    context = {
        'inv': inv, 'form': form, 'page':'det',
        'title': 'Altera Rekomendasaun Pagamentu', 'legend': 'Altera Rekomendasaun Pagamentu'
    }
    return render(request, 'inv_recom/form.html', context)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipRecomRem(request, pk):
    obj = get_object_or_404(PayRecom, pk=pk)
    inv = obj.inv
    obj.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('uvip-inv-det', hashid=inv.hashed)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipRecomLock(request, pk):
    obj = get_object_or_404(PayRecom, pk=pk)
    inv = obj.inv
    obj.is_lock = True
    obj.save()
    messages.success(request, f'Apaga ona.')
    return redirect('uvip-recom-det', hashid=obj.hashed)
###
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opRecomContList(request):
    group = request.user.groups.all()[0].name
    objects = Contract.objects.filter().all().order_by("-id")
    context = {
        'group': group, 'objects': objects, 'module_name': 'Modulu Rekomendasaun Pagamentu', 
        'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
    }
    return render(request, 'inv_recom/op_cont_list.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opRecomList(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    objects = PayRecom.objects.filter(cont=cont).all()
    tot = PayRecom.objects.filter(cont=cont).aggregate(Sum('amount')).get('amount__sum', 0.00)
    context = {
        'group': group, 'cont': cont, 'objects': objects, 'tot': tot, 'module_name': 'Modulu Rekomendasaun Pagamentu', 
        'title': 'Lista Rekomendasaun', 'legend': 'Lista Rekomendasaun',
    }
    return render(request, 'inv_recom/op_recom_list.html', context)
#
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opRecomAdd(request, hashid):
    cont = get_object_or_404(Contract, hashed=hashid)
    if request.method == 'POST':
        newid, new_hashid = getnewid(PayRecom)
        form = PayRecomForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.cont = cont
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('op-recom-list', hashid=hashid)
    else: form = PayRecomForm()
    context = {
        'cont': cont, 'form': form,
        'title': 'Aumenta Rekomendasaun Pagamentu', 'legend': 'Aumenta Rekomendasaun Pagamentu'
    }
    return render(request, 'inv_recom/op_form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opRecomEdit(request, hashid, pk):
    objects = get_object_or_404(PayRecom, pk=pk)
    cont = objects.contract
    if request.method == 'POST':
        form = PayRecomForm(request.POST, request.FILES, instance=objects)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('op-recom-list', hashid=hashid)
    else: form = PayRecomForm(instance=objects)
    context = {
        'cont': cont, 'form': form,
        'title': 'Altera Rekomendasaun Pagamentu', 'legend': 'Altera Rekomendasaun Pagamentu'
    }
    return render(request, 'inv_recom/op_form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opRecomRem(request, hashid, pk):
    objects = get_object_or_404(PayRecom, pk=pk)
    objects.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('op-recom-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opRecomLock(request, hashid, pk):
    objects = get_object_or_404(PayRecom, pk=pk)
    objects.is_lock = True
    objects.save()
    messages.success(request, f'Xavi ona.')
    return redirect('op-recom-list', hashid=hashid)