from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from contract.models import ContractComp
from eval.models import Eval
from ver.models import Ver, VerSecEng,VerSecEngEmployee
from conf.user_utils import c_user_sec, c_user_eng

@allowed_users(allowed_roles=['sigp_admin','sigp_uivp','sigp_gabm','sigp_min','sigp_dgaf'])
def VerList(request):
    group = get_roles(request)
    objects = Ver.objects.filter().all()
    context = {
        'group': group, 'objects': objects,
        'title': 'Lista Verifikasaun', 'legend': 'Lista  Verifikasaun'
    }
    return render(request, 'ver/ver_list.html', context)
#
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipVerList(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    proj = eval.proj
    objects = Ver.objects.filter(eval=eval).all()
    context = {
        'group': group, 'eval':eval, 'proj': proj, 'objects': objects,
        'title': 'Lista Despaxu ba Sekasaun', 'legend': 'Lista Despaxu ba Sekasaun'
    }
    return render(request, 'ver/uvip_list.html', context)

@allowed_users(allowed_roles=['sigp_uivp'])
def uvipVerDet(request, hashid):
    group = get_roles(request)
    ver = get_object_or_404(Ver, hashed=hashid)
    eval = ver.eval
    proj = eval.proj
    objects = VerSecEng.objects.filter(ver=ver).all()
    objects1 = VerSecEngEmployee.objects.all()
    
    context = {
        'group':group, 'ver':ver, 'eval':eval,  'proj':proj, 'objects':objects,'objects1':objects1,
        'title': 'Detallu Despaxu ba Seksaun', 'legend': 'Detallu Despaxu ba Seksaun'
    }
    return render(request, 'ver/uvip_det.html', context)

# sec
def secVerList(request):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    objects = Ver.objects.filter(sec=sec).all().order_by('-start_date')
    years = Ver.objects.filter(sec=sec).distinct().values('start_date__year').all()
    context = {
        'group': group, 'objects': objects, 'years': years,
        'title': 'Lista Despaxu Verifikasaun', 'legend': 'Lista Despaxu Verifikasaun'
    }
    return render(request, 'ver/sec_list.html', context)

def secVerYear(request, year):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    objects = Ver.objects.filter(sec=sec, start_date__year=year).all().order_by('-start_date')
    years = Ver.objects.filter(sec=sec).distinct().values('start_date__year').all()
    context = {
        'group': group, 'objects': objects, 'years': years,
        'title': f'Despaxu ba Verifikasaun Tinan {year}', 'legend': f'Despaxu ba Verifikasaun Tinan {year}'
    }
    return render(request, 'ver/sec_list.html', context)

def secVerDet(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    ver = get_object_or_404(Ver, hashed=hashid)
    eval = ver.eval
    proj = eval.proj
    objects = VerSecEng.objects.filter(ver=ver).all().order_by('id')
    print("objects",objects)
    emp=[]
    b = 0
    for a in objects:
        b=a.to.all()
    emp.append(str(b)[0])
    object1 = VerSecEngEmployee.objects.all()
    context = {
        'group': group, 'eval': eval, 'proj': proj, 'ver': ver,'emp':emp,
        'objects': objects, 'object1':object1, 'page': 'sec',
        'title': 'Despaxu ba Enjeneiru', 'legend': 'Despaxu ba Enjeneiru'
    }
    return render(request, 'ver/sec_det.html', context)
# eng
def engVerList(request):
    group = get_roles(request)
    eng = c_user_eng(request.user)
    objects = VerSecEng.objects.filter(to=eng).all().order_by('-date')
    object1 = VerSecEngEmployee.objects.all()
    years = VerSecEng.objects.filter(to=eng).distinct().values('date__year').all()
    context = {
        'group': group, 'objects': objects, 'object1':object1, 'years': years,
        'title': 'Despaxu Tama', 'legend': 'Despaxu Tama'
    }
    return render(request, 'ver/eng_list.html', context)

def engVerYear(request, year):
    group = get_roles(request)
    eng = c_user_eng(request.user)
    objects = VerSecEng.objects.filter(to=eng).all().order_by('-date')
    years = VerSecEng.objects.filter(to=eng).distinct().values('date__year').all()
    context = {
        'group': group, 'objects': objects, 'years': years,
        'title': f'Despaxu Tama Tinan {year}', 'legend': f'Despaxu Tama Tinan {year}'
    }
    return render(request, 'ver/eng_list.html', context)

def engVerDet(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    versec = get_object_or_404(VerSecEng, hashed=hashid)
    ver = versec.ver
    eval = ver.eval
    proj = eval.proj
    object1 = VerSecEngEmployee.objects.all()
    context = {
        'group': group, 'eval':eval,  'proj': proj, 
        'versec': versec, 'ver': ver, 'object1':object1,
        'title': 'Komentariu Enjeneiru', 'legend': 'Komentariu Enjeneiru'
    }
    return render(request, 'ver/eng_det.html', context)
# all

@allowed_users(allowed_roles=['sigp_admin','sigp_gabm','sigp_dna','sigp_dnof','sigp_min','sigp_dgaf','sigp_uivp'])
def allVerList(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    comps = ContractComp.objects.filter(contract=cont).all()
    objects = Ver.objects.filter(cont=cont).all()
    context = {
        'group': group, 'inv':inv, 'cont': cont, 'proj': proj, 'objects': objects, 'comps': comps,
        'title': 'Lista Despaxu', 'legend': 'Lista Despaxu'
    }
    return render(request, 'ver/all_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_gabm','sigp_dna','sigp_dnof','sigp_min','sigp_dgaf'])
def allVerDet(request, hashid):
    group = get_roles(request)
    ver = get_object_or_404(Ver, hashed=hashid)
    inv = ver.inv
    cont = ver.cont
    proj = cont.project
    comps = ContractComp.objects.filter(contract=cont).all()
    objects = VerSecEng.objects.filter(ver=ver).all()
    context = {
        'group': group, 'ver':ver, 'inv':inv, 'cont': cont, 'proj': proj, 'objects': objects,
        'comps': comps,
        'title': 'Detallu Despaxu', 'legend': 'Detallu Despaxu'
    }
    return render(request, 'ver/all_det.html', context)