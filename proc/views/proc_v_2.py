import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Q
from proc.models import Proc, ProcComp, ProcLet, ProcTrack, ProcReqTrack, ProcResTrack
from conf.user_utils import c_user_dgaf, c_user_dna, c_user_min, c_user_vice
from users.decorators import allowed_users
from sigp.utils import get_roles

### DGAF
@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcList(request):
	group = get_roles(request)
	objects = Proc.objects.filter().all().order_by("-datetime","id")
	context = {
		'group':group, 'objects':objects,
		'title':'Lista Tender', 'legend':'Lista Tender'
	}
	return render(request, 'proc_dgaf/list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcDet(request, hashid):
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
		'title': 'Detalha Tender', 'legend': 'Detalha Tender',
	}
	return render(request, 'proc_dgaf/detail.html', context)
# req
@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcReqList(request):
	group = get_roles(request)
	objects = Proc.objects.filter(is_req_start=True).all().order_by("-id")
	context = {
		'group':group, 'objects':objects,
		'title': 'Lista Rekizasaun Tender', 'legend': 'Lista Rekizasaun Tender'
	}
	return render(request, 'proc_dgaf/req_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcReqDet(request, hashid):
	group = get_roles(request)
	proc = get_object_or_404(Proc, hashed=hashid)
	proj = proc.proj
	track = ProcReqTrack.objects.filter(proc=proc).last()
	lets1 = ProcLet.objects.filter(proc=proc, is_req=True, is_dgaf=True).all().order_by('-date')
	lets2 = ProcLet.objects.filter(proc=proc, is_req=True, is_dgaf=False).all().order_by('-date')
	context = {
		'group':group, 'proj':proj, 'proc':proc, 'track':track, 'page':'req',
		'lets1':lets1, 'lets2':lets2,
		'title':'Detallu Rekizasaun', 'legend':'Detallu Rekizasaun',
	}
	return render(request, 'proc_dgaf/req_det.html', context)
# res
@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcResList(request):
	group = get_roles(request)
	objects = Proc.objects.filter(is_req_start=True).all().order_by("-id")
	context = {
		'group':group, 'objects':objects,
		'title': 'Lista Rekizasaun Tender', 'legend': 'Lista Rekizasaun Tender'
	}
	return render(request, 'proc_dgaf/res_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcResDet(request, hashid):
	group = get_roles(request)
	proc = get_object_or_404(Proc, hashed=hashid)
	proj = proc.proj
	comps = ProcComp.objects.filter(proc=proc).all().order_by('best')[:3]
	track = ProcResTrack.objects.filter(proc=proc).last()
	lets1 = ProcLet.objects.filter(proc=proc, is_req=False, is_dgaf=True).all().order_by('-date')
	lets2 = ProcLet.objects.filter(proc=proc, is_req=False, is_dgaf=False).all().order_by('-date')
	context = {
		'group':group, 'proj':proj, 'proc':proc, 'comps':comps, 'track':track, 'page':'res',
		'lets1':lets1, 'lets2':lets2,
		'title':'Detalha Karta', 'legend':'Detalha Karta',
	}
	return render(request, 'proc_dgaf/res_det.html', context)
### GAB
@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_min','sigp_admin'])
def gabProcList(request):
	group = get_roles(request)
	objects = Proc.objects.filter().all().order_by("-date")
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Tender', 'legend': 'Lista Tender'
	}
	return render(request, 'proc_gab/list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_min','sigp_admin'])
def gabProcDet(request, hashid):
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
		'title': 'Detalha Tender', 'legend': 'Detalha Tender',
	}
	return render(request, 'proc_gab/detail.html', context)
# req
@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_min','sigp_admin'])
def gabProcReqList(request):
	group = get_roles(request)
	objects = Proc.objects.filter(is_req_start=True).all().order_by("-id")
	context = {
		'group':group, 'objects':objects,
		'title':'Karta Rekizasaun Tender', 'legend':'Karta Rekizasaun Tender'
	}
	return render(request, 'proc_gab/req_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_min','sigp_admin'])
def gabProcReqDet(request, hashid):
	group = get_roles(request)
	proc = get_object_or_404(Proc, hashed=hashid)
	proj = proc.proj
	track = ProcReqTrack.objects.filter(proc=proc).first()
	lets1 = ProcLet.objects.filter(proc=proc, is_req=True, is_dgaf=True).all().order_by('-date')
	lets2 = ProcLet.objects.filter(proc=proc, is_req=True, is_dgaf=False).all().order_by('-date')
	context = {
		'group':group, 'proj':proj, 'proc':proc, 'track':track, 'page':'req',
		'lets1':lets1, 'lets2':lets2,
		'title':'Detallu Rekizasaun', 'legend':'Detallu Rekizasaun',
	}
	return render(request, 'proc_gab/req_det.html', context)
# res
@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_min','sigp_admin'])
def gabProcResList(request):
	group = get_roles(request)
	objects = Proc.objects.filter(is_res_start=True).all().order_by("-id")
	context = {
		'group':group, 'objects':objects,
		'title':'Lista Rezultadu Tender', 'legend':'Lista Rezultadu Tender'
	}
	return render(request, 'proc_gab/res_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_min','sigp_admin'])
def gabProcResDet(request, hashid):
	group = get_roles(request)
	proc = get_object_or_404(Proc, hashed=hashid)
	proj = proc.proj
	comps = ProcComp.objects.filter(proc=proc).all().order_by('best')[:3]
	track = ProcResTrack.objects.filter(proc=proc).first()
	lets1 = ProcLet.objects.filter(proc=proc, is_req=False, is_dgaf=True).all().order_by('-date')
	lets2 = ProcLet.objects.filter(proc=proc, is_req=False, is_dgaf=False).all().order_by('-date')
	context = {
		'group':group, 'proj':proj, 'proc':proc, 'comps':comps, 'track':track, 'page':'res',
		'lets1':lets1, 'lets2':lets2,
		'title':'Detallu Karta', 'legend':'Detallu Karta',
	}
	return render(request, 'proc_gab/res_det.html', context)
