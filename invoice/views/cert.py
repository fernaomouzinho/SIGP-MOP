import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib import messages
from invoice.models import Invoice, InvTrack, CertPay
from invoice.forms import CertPayForm
from conf.utils import getnewid, write_roman
from users.decorators import allowed_users
from sigp.utils import get_roles

@login_required
def uvipCertDet(request, hashid):
    group = get_roles(request)
    certpay = get_object_or_404(CertPay, hashed=hashid)
    inv = certpay.inv
    track = InvTrack.objects.filter(inv=inv).first()
    context = {
        'group':group, 'inv':inv, 'cont':inv.cont, 'certpay':certpay, 'track':track,
        'title':'Detallu Sertifikadu', 'legend':'Detallu Sertifikadu'
    }
    return render(request, 'inv_cert/detail.html', context)
###
@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipCertAdd(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    if request.method == 'POST':
        newid, new_hashid = getnewid(CertPay)
        form = CertPayForm(request.POST, request.FILES)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        rom_num = write_roman(mt)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            data = form.cleaned_data
            number = data['number']
            instance.number = "%s/%s-MOP/%s/%s" % (number,group.upper(),rom_num,yr)
            instance.inv = inv
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('uvip-cert-det', hashid=new_hashid)
    else: form = CertPayForm()
    context = {
        'group':group, 'inv':inv, 'form':form,
        'title': 'Aumenta Sertifikadu Pagamentu', 'legend': 'Aumenta Sertifikadu Pagamentu'
    }
    return render(request, 'inv_cert/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipCertEdit(request, hashid):
    group = get_roles(request)
    certpay = get_object_or_404(CertPay, hashed=hashid)
    inv = certpay.inv
    if request.method == 'POST':
        form = CertPayForm(request.POST, request.FILES, instance=certpay)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('uvip-cert-det', hashid=hashid)
    else: form = CertPayForm(instance=certpay)
    context = {
        'group':group, 'inv':inv, 'certpay':certpay, 'form':form, 'page':'det',
        'title': 'Altera Sertifikadu Pagamentu', 'legend': 'Altera Sertifikadu Pagamentu'
    }
    return render(request, 'inv_cert/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipCertRem(request, pk):
    obj = get_object_or_404(CertPay, pk=pk)
    inv = obj.inv
    obj.delete()
    messages.success(request, f'Apaga ona.')
    return redirect('uvip-inv-det', hashid=inv.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipCertLock(request, pk):
    obj = get_object_or_404(CertPay, pk=pk)
    obj.is_lock = True 
    obj.save()
    messages.success(request, f'Taka ona.')
    return redirect('uvip-inv-det', hashid=obj.hashed)
