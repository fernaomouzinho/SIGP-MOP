from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from contract.models import Contract,ContractComp, Amendment, AmendmentAmount, Deduction, ContractYear
from payment.models import Invoice, Payment, PaymentFiscal, PaymentHist
from invoice.models import CertPay
from conf.user_utils import c_user_dna
from users.decorators import allowed_users
from sigp.utils import get_roles

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_uivp'])
def dnaPayInvList(request):
    group = get_roles(request)
    dna = c_user_dna(request.user)
    objects = Invoice.objects.filter().all().order_by("-date")
    context = {
        'group': group, 'objects': objects,
        'title': 'Resibu Foun', 'legend': 'Resibu Foun'
    }
    return render(request, 'payment/dna_inv_list.html', context)

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_uivp'])
def dnaPayInvDet(request, hashid):
    group = get_roles(request)
    dna = c_user_dna(request.user)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cert = CertPay.objects.filter(inv=inv).first()
    pays = Payment.objects.filter(invoice=inv).all().order_by('-date')
    context = {
        'group': group, 'inv': inv, 'cert': cert, 'pays': pays,
        'title': 'Detallu Pagamentu', 'legend': 'Detallu Pagamentu'
    }
    return render(request, 'payment/dna_inv_det.html', context)
### CUSTOM

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op', 'sigp_uivp'])
def customPayContList(request):
    group = get_roles(request)
    objects = Contract.objects.filter().all().order_by("-start_date","id")
    objects_1 = ContractComp.objects.filter().all().order_by("id")
    context = {
        'group': group, 'objects': objects,'objects_1':objects_1,
        'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
    }
    return render(request, 'payment/custom_cont_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def customPayList(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    contComp = ContractComp.objects.filter(contract=cont).first()
    pays = Payment.objects.filter(contract=cont).all().order_by("id")
    pay_last = Payment.objects.filter(contract=cont).last()
    amend = Amendment.objects.filter(contract=cont).first()
    amend_a = AmendmentAmount.objects.filter(contract=cont).first()
    deduc = Deduction.objects.filter(contract=cont).first()
    last = Payment.objects.filter(contract=cont).last()
    if last: last = last.com_percent
    else: last = 0
    if pay_last: phys_prog = pay_last.phys_prog
    else: phys_prog = 0
    context = {
        'group': group, 'cont': cont, 'contComp':contComp,'pays': pays, 'phys_prog': phys_prog,
        'amend': amend, 'amend_a': amend_a, 'deduc': deduc, 'info': 'Original', 'last': last,
        'title': 'Lista Pagamentu', 'legend': 'Lista Pagamentu'
    }
    return render(request, 'payment/custom_pay_list.html', context)
### FISCAL

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op', 'sigp_uivp'])
def fiscalPayContList(request):
    group = get_roles(request)
    dna = c_user_dna(request.user)
    objects = Contract.objects.filter(is_fiscal=True).all().order_by("-start_date","id")
    context = {
        'group': group, 'objects': objects,
        'title': 'Lista Kontratu Fiskal', 'legend': 'Lista Kontratu Fiskal'
    }
    return render(request, 'payment/fiscal_cont_list.html', context)

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def fiscalYearList(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    amend = Amendment.objects.filter(contract=cont).first()
    objects = []
    a = cont.start_date.year
    b = cont.end_date.year
    for i in range(a,b+1):
        a = []
        obj = PaymentFiscal.objects.filter(contract=cont, year=i).first()
        if obj: a = obj
        objects.append([i,a])
    context = {
        'group': group, 'cont': cont, 'amend': amend, 'objects': objects,
        'title': 'Tinan Fiskal', 'legend': 'Tinan Fiskal'
    }
    return render(request, 'payment/fiscal_year_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op'])
def fiscalPayList(request, hashid, year):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    contyear = ContractYear.objects.filter(contract=cont, year=year).first()
    fiscal = PaymentFiscal.objects.filter(contract=cont, year=year).first()
    pays = Payment.objects.filter(contyear=contyear).all().order_by("id")
    amend = Amendment.objects.filter(contract=cont).first()
    count = pays.count()
    context = {
        'group': group, 'cont': cont, 'contyear':contyear, 'amend': amend, 'fiscal': fiscal, 'year': year,
        'count':count, 'pays': pays,
        'title': 'Lista Pagamentu Fiskal', 'legend': 'Lista Pagamentu Fiskal'
    }
    return render(request, 'payment/fiscal_pay_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def fiscalPayAll(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    pays = Payment.objects.filter(contract=cont).all().order_by("id")
    amend = Amendment.objects.filter(contract=cont).first()
    context = {
        'group': group, 'cont': cont, 'amend': amend, 'pays': pays,
        'title': 'Lista Pagamentu Fiskal', 'legend': 'Lista Pagamentu Fiskal'
    }
    return render(request, 'payment/fiscal_pay_all.html', context)
### ALL

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op'])
def allPayContList(request):
    group = get_roles(request)
    dna = c_user_dna(request.user)
    objects = Contract.objects.filter().all().order_by("-start_date","id")
    context = {
        'group': group, 'objects': objects,
        'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
    }
    return render(request, 'payment/all_cont_list.html', context)


@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op'])
def allPayList(request, hashid):
    group = get_roles(request)
    dna = c_user_dna(request.user)
    cont = get_object_or_404(Contract, hashed=hashid)
    pays = Payment.objects.filter(contract=cont).all().order_by("id")
    pay_last = Payment.objects.filter(contract=cont).last()
    amend = Amendment.objects.filter(contract=cont).first()
    amend_a = AmendmentAmount.objects.filter(contract=cont).first()
    last = Payment.objects.filter(contract=cont).last()
    if last: last = last.com_percent
    else: last = 0
    if pay_last: phys_prog = pay_last.phys_prog
    else: phys_prog = 0
    context = {
        'group': group, 'cont': cont, 'pays': pays, 'phys_prog': phys_prog,
        'amend': amend, 'amend_a': amend_a, 'info': 'Original', 'last': last,
        'title': 'Lista Pagamentu', 'legend': 'Lista Pagamentu'
    }
    return render(request, 'payment/all_pay_list.html', context)
