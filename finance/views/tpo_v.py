from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from conf.decorators import allowed_users
from project.models import Project, ProjectEst
from contract.models import Contract, ContractComp
from payment.models import Invoice
from finance.models import PO, PRT, EV, TPO
from conf.user_utils import c_user_dnof

@login_required
# @allowed_users(allowed_roles=['dna'])
def TPOContList(request):
    group = request.user.groups.all()[0].name
    dnof = c_user_dnof(request.user)
    objects = Contract.objects.filter().all().order_by("-id")
    context = {
        'group': group, 'objects': objects,
        'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
    }
    return render(request, 'finance_tpo/tpo_cont_list.html', context)

@login_required
# @allowed_users(allowed_roles=['dna'])
def TPOInvList(request, hashid):
    group = request.user.groups.all()[0].name
    dnof = c_user_dnof(request.user)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    comps = ContractComp.objects.filter(contract=cont).all()
    objects = Invoice.objects.filter(cont=cont).all()
    context = {
        'group': group, 'proj': proj, 'cont': cont, 'comps': comps, 'objects': objects,
        'title': 'Lista Resibu', 'legend': 'Lista Resibu',
    }
    return render(request, 'finance_tpo/tpo_inv_list.html', context)

@login_required
# @allowed_users(allowed_roles=['dna'])
def TPOList(request, hashid):
    group = request.user.groups.all()[0].name
    dnof = c_user_dnof(request.user)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    po = PO.objects.filter(inv=inv).first()
    prt = PRT.objects.get(inv=inv)
    ev = EV.objects.get(prt=prt)
    tpo = TPO.objects.filter(inv=inv).first()
    comp = ContractComp.objects.filter(contract=cont).first()
    print(comp.company)
   
    context = {
        'group': group, 'proj': proj, 'cont': cont, 'inv': inv, 'po': po,
        'prt': prt, 'ev': ev, 'tpo': tpo,
        'title': 'Lista TPO', 'legend': 'Lista TPO','comp':comp
    }
    return render(request, 'finance_tpo/tpo_list.html', context)
###