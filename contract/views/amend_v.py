import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from contract.models import Contract, Amendment, AmendmentPeriod, AmendmentAmount, Deduction
from users.decorators import allowed_users
from sigp.utils import get_roles

@login_required
def AmendPerList(request):
    objects = Contract.objects.filter()\
            .prefetch_related('amendment','amendmentperiod').all().order_by("-start_date__year")
    context = {
        'objects': objects,
        'title': 'Amenda Tempu', 'legend': 'Amenda Tempu',
    }
    return render(request, 'amendment/period_list.html', context)

@login_required
def AmendPerDet(request, hashid):
    cont = get_object_or_404(Contract, hashed=hashid)
    amend = Amendment.objects.filter(contract=cont).first()
    proj = cont.project
    objects = AmendmentPeriod.objects.filter(contract=cont).all()
    amend_per = AmendmentPeriod.objects.filter(contract=cont, is_active=True).first()
    context = {
        'cont': cont, 'proj': proj, 'amend': amend, 'objects': objects, 'amend_per': amend_per,
        'title': 'Detallu Amenda', 'legend': 'Detallu Amenda',
    }
    return render(request, 'amendment/period_det.html', context)

@login_required
def AmendAmList(request):
    objects = Contract.objects.filter()\
            .prefetch_related('amendment','amendmentamount').all().order_by("-start_date__year")
    context = {
        'objects': objects,
        'title': 'Amenda Montante', 'legend': 'Amenda Montante',
    }
    return render(request, 'amendment/amount_list.html', context)

@login_required
def AmendAmDet(request, hashid):
    cont = get_object_or_404(Contract, hashed=hashid)
    amend = Amendment.objects.filter(contract=cont).first()
    proj = cont.project
    amds = AmendmentAmount.objects.filter(contract=cont).all()
    objects = []
    for i in amds:
        a = float(i.total)
        b = float(cont.total)*0.1
        c = round((a*100)/float(cont.total),2)
        x = False
        if float(a) > float(b): x = True
        objects.append([i,x,c])
    print(objects)
    context = {
        'cont': cont, 'amend': amend, 'proj': proj, 'objects': objects, 'page': 'amount',
        'title': 'Detallu Amenda', 'legend': 'Detallu Amenda',
    }
    return render(request, 'amendment/amount_det.html', context)

@login_required
def DeducList(request):
    objects = Contract.objects.filter()\
            .prefetch_related('amendment','deduction').all().order_by("-start_date__year")
    context = {
        'objects': objects,
        'title': 'Dedusaun', 'legend': 'Dedusaun',
    }
    return render(request, 'amendment/deduc_list.html', context)

@login_required
def DeducDet(request, hashid):
    cont = get_object_or_404(Contract, hashed=hashid)
    amend = Amendment.objects.filter(contract=cont).first()
    proj = cont.project
    objs = Deduction.objects.filter(contract=cont).all()
    objects = []
    for i in objs:
        a = float(cont.total)-float(i.total)
        print(a)
        b = round((a*100)/float(cont.total),2)
        print(b)
        x = False
        if float(a) > float(b): x = True
        objects.append([i,x,b])
    context = {
        'cont': cont, 'amend': amend, 'proj': proj, 'objects': objects, 'page': 'deduc',
        'title': 'Detallu Dedusaun', 'legend': 'Detallu Dedusaun',
    }
    return render(request, 'amendment/deduc_det.html', context)
