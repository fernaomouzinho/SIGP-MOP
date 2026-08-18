from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from project.models import Project
from proc.models import Proc, ProcComp, ProcLet, ProcReqTrack, ProcResTrack, ProcTrack
from conf.user_utils import c_user_div
from users.decorators import allowed_users
from sigp.utils import get_roles

### DNA
@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_uivp','sigp_admin'])
def dnaProcList(request):
    group = get_roles(request)
    objects = Proc.objects.filter().all().order_by("-id")
    context = {
        'group':group, 'objects':objects,
        'title':'Lista Tender', 'legend':'Lista Tender'
    }
    return render(request, 'proc_dna/list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcDet(request, hashid):
    group = get_roles(request)
    proc = get_object_or_404(Proc, hashed=hashid)
    proj = proc.proj
    comps = ProcComp.objects.filter(proc=proc).all()
    track = ProcTrack.objects.filter(proc=proc).first()
    trackreq = ProcReqTrack.objects.filter(proc=proc).first()
    trackres = ProcResTrack.objects.filter(proc=proc).first()
    context = {
        'group':group, 'proj':proj, 'proc':proc, 'comps':comps,
        'track':track, 'trackreq':trackreq, 'trackres':trackres, 
        'title': 'Detalha Tender', 'legend': 'Detallu Tender',
    }
    return render(request, 'proc_dna/detail.html', context)
# req
@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcReqList(request):
    group = get_roles(request)
    objects = Proc.objects.filter(is_req_start=True).all().order_by("-id")
    context = {
        'group':group, 'objects':objects,
        'title': 'Lista Rekizasaun Tender', 'legend': 'Lista Rekizasaun Tender'
    }
    return render(request, 'proc_dna/req_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcReqDet(request, hashid):
    group = get_roles(request)
    proc = get_object_or_404(Proc, hashed=hashid)
    proj = proc.proj
    lets = ProcLet.objects.filter(proc=proc, is_req=True).all().order_by("-date","id")	
    track = ProcReqTrack.objects.filter(proc=proc).last()
    context = {
        'group': group, 'proj':proj, 'proc':proc, 'lets':lets, 'track':track, 'page':'req',
        'title': 'Detallu Rekizasaun Tender', 'legend': 'Detallu Rekizasaun Tender',
    }
    return render(request, 'proc_dna/req_det.html', context)
# res
@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcResList(request):
    group = get_roles(request)
    objects = Proc.objects.filter(is_res_start=True).all().order_by("-id")
    context = {
        'group': group, 'objects': objects,
        'title': 'Lista Resultadu Tender', 'legend': 'Lista Rezultadu Tender'
    }
    return render(request, 'proc_dna/res_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcResDet(request, hashid):
    group = get_roles(request)
    proc = get_object_or_404(Proc, hashed=hashid)	
    comps = ProcComp.objects.filter(proc=proc).all().order_by('best')
    proj = proc.proj
    lets = ProcLet.objects.filter(proc=proc, is_req=False).all().order_by("-date","id")	
    track = ProcResTrack.objects.filter(proc=proc).last()
    context = {
        'group': group, 'proj':proj, 'proc':proc, 'comps':comps, 'lets':lets, 'track':track, 'page':'res',
        'title': 'Resultadu Tender', 'legend': 'Resultadu Tender',
    }
    return render(request, 'proc_dna/res_det.html', context)
# div
@login_required
@allowed_users(allowed_roles=['sigp_div','sigp_admin'])
def divProcList(request):
    group = get_roles(request)
    div = c_user_div(request.user)
    objects = Proc.objects.filter(proj__owner=div, is_res_start=True).all().order_by("-id")
    context = {
        'group': group, 'objects': objects,
        'title': 'Lista Projetu', 'legend': 'Lista Projetu'
    }
    return render(request, 'proc_div/list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_div','sigp_admin'])
def divProcDet(request, hashid):
    group = get_roles(request)
    proc = get_object_or_404(Proc, hashed=hashid)	
    comps = ProcComp.objects.filter(proc=proc).all().order_by('best')
    proj = proc.proj
    lets = ProcLet.objects.filter(proc=proc, is_req=False).all().order_by("-date","id")	
    track = ProcResTrack.objects.filter(proc=proc).last()
    context = {
        'group': group, 'proj':proj, 'proc':proc, 'comps':comps, 'lets':lets, 'track':track, 'page':'res',
        'title': 'Rezultadu Tender', 'legend': 'Rezultadu Tender',
    }
    return render(request, 'proc_div/det.html', context)