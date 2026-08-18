import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib import messages
from project.models import Project
from contract.models import Contract, Amendment, AmendmentAmount, ContractYear
from payment.models import Invoice, Payment
from payment.forms import PayForm
from invoice.models import CertPay
from payment.pay_utils import f_com_amount, f_com_percent, f_bal_amount, f_bal_percent, f_refresh
from conf.utils import getnewid
from users.decorators import allowed_users
from sigp.utils import get_roles

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s'])
def dnaPayAdd(request, hashid):
    inv = get_object_or_404(Invoice, hashed=hashid)
    cert = CertPay.objects.filter(inv=inv).first()
    cont = inv.cont
    hashid=hashid
    amend = Amendment.objects.filter(contract=cont).first()
    contyear = ContractYear.objects.filter(contract=cont).first()
    paylast = Payment.objects.filter(contract=cont).last()
    if paylast: pay_com = paylast.com_amount
    else: pay_com = 0
    if request.method == 'POST':
        newid, new_hashid = getnewid(Payment)
        form = PayForm(request.POST)
        if form.is_valid():
            com_amount = f_com_amount(cert.total,pay_com)
            com_percent = f_com_percent(com_amount,amend.total)
            bal_amount = f_bal_amount(amend.total,com_amount)
            bal_percent = f_bal_percent(bal_amount,amend.total)
            instance = form.save(commit=False)
            instance.id = newid
            instance.contract = cont
            instance.contyear = contyear
            instance.invoice = inv
            instance.phys_prog = cert.phys_prog
            instance.total = cert.total
            instance.date = cert.date
            instance.com_amount = com_amount
            instance.com_percent = com_percent
            instance.bal_amount = bal_amount
            instance.bal_percent = bal_percent
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('dna-pay-inv-det', hashid=hashid)
    else: form = PayForm()
    context = {
        'inv': inv, 'form': form, 'page': 'invpay', 'cert':cert,'hashid':hashid,
        'title': 'Aumenta Pagamentu', 'legend': 'Aumenta Pagamentu'
    }
    return render(request, 'payment/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s'])
def dnaPayEdit(request, hashid, hashid2):
    inv = get_object_or_404(Invoice, hashed=hashid)
    hashid=hashid
    contyear = ContractYear.objects.filter(contract=inv.cont).first()
    pay = get_object_or_404(Payment, hashed=hashid2)
    cert = CertPay.objects.filter(inv=inv).first()
    if request.method == 'POST':
        form = PayForm(request.POST, instance=pay)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.contyear = contyear
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('dna-pay-inv-det', hashid=hashid)
    else: form = PayForm(instance=pay)
    context = {
        'cert': cert, 'form': form, 'hashid':hashid,
        'title': 'Altera Pagamentu', 'legend': 'Altera Pagamentu'
    }
    return render(request, 'payment/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s'])
def dnaPayRem(request, hashid, pk):
    objects = get_object_or_404(Payment, pk=pk)
    objects.delete()
    messages.success(request, f'Hapaga ona!')
    return redirect('dna-pay-inv-det', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s'])
def dnaPayLock(request, hashid, pk):
    objects = get_object_or_404(Payment, pk=pk)
    objects.is_lock = True
    objects.save()
    messages.success(request, f'Xavi.')
    return redirect('dna-pay-inv-det', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s'])
def dnaPayUnLock(request, hashid, pk):
    objects = get_object_or_404(Payment, pk=pk)
    objects.is_lock = False
    objects.save()
    messages.success(request, f'Loke.')
    return redirect('dna-pay-inv-det', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s'])
def dnaPayReady(request, hashid, pk):
    inv = get_object_or_404(Invoice, hashed=hashid)
    inv.is_paid = True
    inv.save()
    objects = get_object_or_404(Payment, pk=pk)
    objects.is_ready = True
    objects.save()
    messages.success(request, f'Pronto.')
    return redirect('dna-pay-inv-det', hashid=hashid)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s'])
def dnaPayRefresh(request, hashid):
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.contract
    amend = Amendment.objects.filter(contract=cont).first()
    pays = Payment.objects.filter(contract=cont).all()
    amend_amount = float(amend.total)

    payment2 = f_refresh(pays)
    zeros = np.array([np.zeros(payment2.shape[1])])
    new_payment = np.array(np.vstack((zeros,payment2)))
    new_result = []
    for i in range(1,new_payment.shape[0]):
        id = new_payment[i,0]
        amount = float(new_payment[i,1])
        pay_com = float(new_payment[i-1,2])
        com_amount = f_com_amount(amount,pay_com)
        com_percent = f_com_percent(com_amount,amend_amount)
        bal_amount = f_bal_amount(amend_amount,com_amount)
        bal_percent = f_bal_percent(bal_amount,amend_amount)
        new_result.append([id,com_amount,com_percent,bal_amount,bal_percent])
    for j in new_result:
        obj = Payment.objects.filter(id=j[0]).first()
        obj.com_amount = j[1]
        obj.com_percent = j[2]
        obj.bal_amount = j[3]
        obj.bal_percent = j[4]
        obj.save()
    messages.success(request, f'Altera ona.')
    return redirect('dna-pay-inv-det', hashid=hashid)
