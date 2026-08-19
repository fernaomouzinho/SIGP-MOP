import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import FileResponse, Http404
from contract.models import Contract, ContractComp, ContractFiles, Amendment, ContractYear
from finance.models import CPV
from conf.user_utils import c_user_div, c_user_sup
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op','sigp_gab','sigp_uivp'])
def dnaContList(request):
    group = get_roles(request)
    conts = Contract.objects.filter().all().order_by('-start_date','id')
    objects = []
    for i in conts:
        a = Amendment.objects.filter(contract=i).first()
        print(a)
        objects.append([i,a])
    context = {
        'group': group, 'objects': objects,
        'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
    }
    return render(request, 'contract/dna_cont_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op','sigp_gab','sigp_uivp'])
def dnaContDet(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    powner = proj.owner
    amend = Amendment.objects.filter(contract=cont).first()
    comps = ContractComp.objects.filter(contract=cont).all()
    files = ContractFiles.objects.filter(contract=cont).all()
    contyears = ContractYear.objects.filter(contract=cont).all()
    cpv = CPV.objects.filter(proj=proj).last()
    context = {
        'group': group, 'proj': proj, 'powner': powner, 'cont': cont, 'amend': amend, 'comps': comps,
        'files': files, 'contyears':contyears, 'cpv': cpv,
        'title': 'Detalha Kontratu', 'legend': 'Detalha Kontratu'
    }
    return render(request, 'contract/dna_cont_det.html', context)
### ALL

def ContList(request):
    group = get_roles(request)
    div = c_user_div(request.user)

    if 'sigp_div' in group:
        conts = Contract.objects.filter(project__owner=div).all().order_by('-start_date','id')
    else:
        conts = Contract.objects.filter().all().order_by('-start_date','id')
    # conts = Contract.objects.filter().all().order_by('-start_date','id')
    objects = []
    for i in conts:
        a = Amendment.objects.filter(contract=i).first()
        objects.append([i,a])
    context = {
        'group': group, 'objects': objects,
        'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
    }
    return render(request, 'contract/cont_list.html', context)


def ContDet(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    powner = proj.owner
    amend = Amendment.objects.filter(contract=cont).first()
    comps = ContractComp.objects.filter(contract=cont).all()
    files = ContractFiles.objects.filter(contract=cont).all()
    context = {
        'group': group, 'proj': proj, 'powner': powner, 'cont': cont, 'amend': amend, 'comps': comps,
        'files': files,
        'title': 'Detalha Kontratu', 'legend': 'Detalha Kontratu'
    }
    return render(request, 'contract/cont_det.html', context)
###

def ContPDF(request, pk):
    group = get_roles(request)
    objects = get_object_or_404(ContractFiles, pk=pk)
    file = str(settings.BASE_DIR)+str(objects.file.url)
    try:
        if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
        else: return FileResponse(open(file, 'rb'))
    except FileNotFoundError: raise Http404('not found')
#

def ContMonitorList(request):
    group = get_roles(request)
    div = c_user_div(request.user)
    today = datetime.date.today()
    if group == "div":
        obj = Contract.objects.filter(project__owner=div, is_complete=False).all().order_by('-start_date','id')
    else:
        obj = Contract.objects.filter(is_complete=False).all().order_by('-start_date','id')
    objects = []
    for i in obj:
        amend = Amendment.objects.filter(contract=i).first()
        if today < amend.end_date:
            d = (amend.end_date-today).days
            e = "-"
            f = False
        else:
            d = (today-amend.end_date).days
            e = "+"
            f = True
        objects.append([i,amend,d,e,f])
    context = {
        'group': group, 'objects': objects,
        'title': 'Monitor Kontratu', 'legend': 'Monitor Kontratu'
    }
    return render(request, 'contract/monitor_list.html', context)
###

@allowed_users(allowed_roles=['sigp_sup'])
def supContList(request):
    group = get_roles(request)
    mun = c_user_sup(request.user)
    conts = Contract.objects.filter(project__projectloc__municipality=mun).all().order_by("-id")
    objects = []
    for i in conts:
        a = Amendment.objects.filter(contract=i).first()
        objects.append([i,a])
    context = {
        'group': group, 'objects': objects,
        'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
    }
    return render(request, 'contract/sup_cont_list.html', context)
