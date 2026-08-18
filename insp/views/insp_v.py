from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from contract.models import ContractComp
from invoice.models import Invoice
from insp.models import Insp, InspSecEng,InspSecEngEmployee, InspTracks
from conf.user_utils import c_user_sec, c_user_eng,c_user_pos
from users.decorators import allowed_users
from sigp.utils import get_roles


@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_uivp','sigp_gab','sigp_min','sigp_dgaf'])
def InspInvList(request):
    group = get_roles(request)
    objects = Invoice.objects.filter().all().order_by('-date')
    context = {
        'group': group, 'objects': objects,
        'title': 'Lista Resibu ba Inspeksaun', 'legend': 'Lista Resibu ba Inspeksaun'
    }
    return render(request, 'insp/inv_list.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipInspList(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    comps = ContractComp.objects.filter(contract=cont).all()
    objects = Insp.objects.filter(cont=cont).all()
    context = {
        'group': group, 'inv':inv, 'cont': cont, 'proj': proj, 'objects': objects, 'comps': comps,
        'title': 'Lista Despaxu ba Sekasaun', 'legend': 'Lista Despaxu  ba Sekasaun'
    }
    return render(request, 'insp/uvip_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipInspDet(request, hashid):
    group = get_roles(request)
    insp = get_object_or_404(Insp, hashed=hashid)
    inv = insp.inv
    cont = insp.cont
    proj = cont.project
    insptrack = InspTracks.objects.filter(insp=insp).first()
    comps = ContractComp.objects.filter(contract=cont).all()
    objects = InspSecEng.objects.filter(insp=insp).all()
    objects1 = InspSecEngEmployee.objects.all()
    
    context = {
        'group':group, 'insp':insp, 'insptrack':insptrack,'inv':inv, 'cont':cont, 'proj':proj, 'objects':objects,'objects1':objects1,
        'comps':comps,
        'title': 'Detallu Despaxu ba Seksaun', 'legend': 'Detallu Despaxu ba Seksaun'
    }
    return render(request, 'insp/uvip_det.html', context)
# sec
@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspList(request):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    epos = c_user_pos(request.user)
    
    objects = Insp.objects.filter(epos__cat=epos,sec=sec,).all().order_by('-start_date')
    years = Insp.objects.filter(epos__cat=epos,sec=sec,).distinct().values('start_date__year').all()
    
    context = {
        'group': group, 'objects': objects, 'years': years,
        'title': 'Lista Despaxu Inspeksaun', 'legend': 'Lista Despaxu Inspeksaun'
    }
    return render(request, 'insp/sec_list.html', context)

@login_required
def secInspYear(request, year):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    epos = c_user_pos(request.user)
    objects = Insp.objects.filter(epos__cat=epos, start_date__year=year).all().order_by('-start_date')
    years = Insp.objects.filter(epos__cat=epos).distinct().values('start_date__year').all()
    context = {
        'group': group, 'objects': objects, 'years': years,
        'title': f'Despaxu ba Inspeksaun Tinan {year}', 'legend': f'Despaxu ba Inspeksaun Tinan {year}'
    }
    return render(request, 'insp/sec_list.html', context)

@login_required
def secInspDet(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    epos = c_user_pos(request.user)
    insp = get_object_or_404(Insp, hashed=hashid)
    inv = insp.inv
    cont = insp.cont
    proj = cont.project
    comps = ContractComp.objects.filter(contract=cont).all()
    objects = InspSecEng.objects.filter(insp=insp).all().order_by('id')
    object1 = InspSecEngEmployee.objects.all()
    context = {
        'group': group, 'inv': inv, 'cont': cont, 'proj': proj, 'comps': comps, 'insp': insp,
        'objects': objects, 'object1':object1, 'page': 'sec',
        'title': 'Despaxu ba Enjeneiru', 'legend': 'Despaxu ba Enjeneiru'
    }
    return render(request, 'insp/sec_det.html', context)
# eng
@login_required
@allowed_users(allowed_roles=['sigp_eng','sigp_admin'])
def engInspList(request):
    group = get_roles(request)
    eng = c_user_eng(request.user)
    epos = c_user_pos(request.user)
    objects = InspSecEng.objects.filter(to=eng, insp__epos__cat=epos).all().order_by('-date')
    object1 = InspSecEngEmployee.objects.all()
    years = InspSecEng.objects.filter(to=eng, insp__epos__cat=epos).distinct().values('date__year').all()
    
    context = {
        'group': group, 'objects': objects, 'object1':object1, 'years': years,
        'title': 'Despaxu Tama', 'legend': 'Despaxu Tama'
    }
    return render(request, 'insp/eng_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_eng','sigp_admin'])
def engInspYear(request, year):
    group = get_roles(request)
    eng = c_user_eng(request.user)
    epos = c_user_pos(request.user)
    objects = InspSecEng.objects.filter(to=eng, insp__epos__cat=epos).all().order_by('-date')
    years = InspSecEng.objects.filter(to=eng, insp__epos__cat=epos).distinct().values('date__year').all()
    context = {
        'group': group, 'objects': objects, 'years': years,
        'title': f'Despaxu Tama Tinan {year}', 'legend': f'Despaxu Tama Tinan {year}'
    }
    return render(request, 'insp/eng_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_eng','sigp_admin'])
def engInspDet(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    inspsec = get_object_or_404(InspSecEng, hashed=hashid)
    insp = inspsec.insp
    inv = insp.inv
    cont = insp.cont
    proj = cont.project
    comps = ContractComp.objects.filter(contract=cont).all()
    object1 = InspSecEngEmployee.objects.all()
    context = {
        'group': group, 'inv':inv, 'cont': cont, 'proj': proj, 'comps': comps,
        'inspsec': inspsec, 'insp': insp, 'object1':object1,
        'title': 'Komentariu Enjeneiru', 'legend': 'Komentariu Enjeneiru'
    }
    return render(request, 'insp/eng_det.html', context)
# all
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_gabm','sigp_dna','sigp_dnof','sigp_min','sigp_dgaf','sigp_uivp'])
def allInspList(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    comps = ContractComp.objects.filter(contract=cont).all()
    objects = Insp.objects.filter(cont=cont).all()
    context = {
        'group': group, 'inv':inv, 'cont': cont, 'proj': proj, 'objects': objects, 'comps': comps,
        'title': 'Lista Despaxu', 'legend': 'Lista Despaxu'
    }
    return render(request, 'insp/all_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin','sigp_gabm','sigp_dna','sigp_dnof','sigp_min','sigp_dgaf'])
def allInspDet(request, hashid):
    group = get_roles(request)
    insp = get_object_or_404(Insp, hashed=hashid)
    inv = insp.inv
    cont = insp.cont
    proj = cont.project
    comps = ContractComp.objects.filter(contract=cont).all()
    objects = InspSecEng.objects.filter(insp=insp).all()
    context = {
        'group': group, 'insp':insp, 'inv':inv, 'cont': cont, 'proj': proj, 'objects': objects,
        'comps': comps,
        'title': 'Detallu Despaxu', 'legend': 'Detallu Despaxu'
    }
    return render(request, 'insp/all_det.html', context)