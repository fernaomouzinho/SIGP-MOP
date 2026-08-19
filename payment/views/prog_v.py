from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from contract.models import Contract, Amendment, AmendmentAmount, ContractComp
from payment.models import Invoice, Payment, PaymentHist, PhysicalProgress
from conf.user_utils import c_user_dna
from users.decorators import allowed_users
from sigp.utils import get_roles

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_uivp'])
def ProgList(request):
    group = get_roles(request)
    dna = c_user_dna(request.user)
    conts = Contract.objects.filter().all().order_by("-start_date","id")
    objects = []
    for i in conts:
        a = Payment.objects.filter(contract=i).last()
        b = PhysicalProgress.objects.filter(contract=i).last
        c = ContractComp.objects.filter(contract=i).last()
        objects.append([i,a,b,c])
    years = Contract.objects.filter().distinct().values('start_date__year').all()
    context = {
        'group': group, 'objects': objects, 'years': years,
        'title': 'Lista Progresu', 'legend': 'Lista Progresu'
    }
    return render(request, 'progress/list.html', context)

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_uivp'])
def ProgYearList(request, year):
    group = get_roles(request)
    dna = c_user_dna(request.user)
    conts = Contract.objects.filter(start_date__year=year).all().order_by("-start_date","id")
    objects = []
    for i in conts:
        a = Payment.objects.filter(contract=i).last()
        objects.append([i,a])
    years = Contract.objects.filter().distinct().values('start_date__year').all()
    context = {
        'group': group, 'objects': objects, 'years': years,
        'title': f'Lista Progresu Tinan {year}', 'legend': f'Lista Progresu Tinan {year}'
    }
    return render(request, 'progress/list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_uivp'])
def PhysicalProgList(request, hashid):
    group = get_roles(request)
    dna = c_user_dna(request.user)
    cont = get_object_or_404(Contract, hashed=hashid)
    phy_prog= PhysicalProgress.objects.filter(contract=cont).all().order_by("id")
    years = Contract.objects.filter().distinct().values('start_date__year').all()
    context = {
        'group': group, 'objects': phy_prog, 'cont':cont, 'years': years,
        'title': 'Lista Progresu Fiziku', 'legend': 'Lista Progresu Fiziku'
    }
    return render(request, 'progress/phy_list.html', context)