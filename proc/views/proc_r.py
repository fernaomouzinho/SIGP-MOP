from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Q
from proc.models import Proc, ProcComp, ProcLet, ProcTrack
from conf.user_utils import c_user_dg, c_user_dgaf, c_user_div, c_user_dna, c_user_min
from project.models import Project
from users.decorators import allowed_users
from sigp.utils import get_roles

### MIN

@allowed_users(allowed_roles=['sigp_min','sigp_admin'])
def rMINProcLetDet(request, hashid):
	group = get_roles(request)
	min = c_user_min(request.user)
	letmin = get_object_or_404(ProcLet, hashed=hashid)
	proj = letmin.project
	proc = letmin.proc
	comps = ProcComp.objects.filter(proc=proc).all().order_by('best')
	if letmin.is_req == True:
		objects = ProcLetter.objects.filter((Q(is_div=True)|Q(is_dgaf=True)), proc=proc, is_req=True).all()
	else:
		objects = ProcLetter.objects.filter((Q(is_div=True)|Q(is_dgaf=True)), proc=proc, is_req=False).all()
	context = {
		'group': group, 'proj': proj, 'proc': proc, 'letmin': letmin, 'objects': objects, 'comps': comps,
		'title': 'Detallu Karta', 'legend': 'Detallu Karta',
	}
	return render(request, 'proc_r/min_det.html', context)

@allowed_users(allowed_roles=['sigp_min','sigp_admin'])
def rMINProcLetList(request):
	group = get_roles(request)
	min = c_user_min(request.user)
	objects = ProcLetter.objects.filter(is_min=True).all().order_by("-date")
	years = ProcLetter.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Despaisu Ministru', 'legend': f'Despaisu Ministru'
	}
	return render(request, 'proc_r/min_list.html', context)

@allowed_users(allowed_roles=['sigp_min','sigp_admin'])
def rMINProcLetYear(request, year):
	group = get_roles(request)
	min = c_user_min(request.user)
	objects = ProcLetter.objects.filter(is_min=True, date__year=year).all().order_by("-date")
	years = ProcLetter.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Despaisu Ministru Tinan {year}', 'legend': f'Despaisu Ministru Tinan {year}'
	}
	return render(request, 'proc_r/min_list.html', context)
### DGAF
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def rDGAFProcLetDet(request, hashid):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	letdgaf = get_object_or_404(ProcLetter, hashed=hashid)
	proj = letdgaf.project
	proc = letdgaf.proc
	comps = ProcComp.objects.filter(proc=proc).all().order_by('best')
	if letdgaf.is_req == True:
		objects = ProcLetter.objects.filter((Q(is_div=True)|Q(is_min=True)), proc=proc, is_req=True).all()
	else:
		objects = ProcLetter.objects.filter((Q(is_div=True)|Q(is_min=True)), proc=proc, is_req=False).all()
	context = {
		'group': group, 'proj': proj, 'proc': proc, 'letdgaf': letdgaf, 'objects': objects, 'comps': comps,
		'title': 'Detallu Karta', 'legend': 'Detalha Karta',
	}
	return render(request, 'proc_r/dgaf_det.html', context)

@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def rDGAFProcLetList(request):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	objects = ProcLetter.objects.filter(is_dgaf=True).all().order_by("-date")
	years = ProcLetter.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Karta DGAF Konaba Tender', 'legend': f'Karta DGAF Konaba Tender'
	}
	return render(request, 'proc_r/dgaf_list.html', context)

@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def rDGAFProcLetYear(request, year):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	objects = ProcLetter.objects.filter(is_dgaf=True, date__year=year).all().order_by("-date")
	years = ProcLetter.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Karta DGAF Konaba Tender Tinan {year}', 'legend': f'Karta DGAF Konaba Tender Tinan {year}'
	}
	return render(request, 'proc_r/dgaf_list.html', context)
### DG
@allowed_users(allowed_roles=['sigp_dg,sigp_admin'])
def rDGProcList(request):
	group = get_roles(request)
	dg = c_user_dg(request.user)
	objects = Project.objects.filter(owner__dg=dg, proc__is_req_start=True).prefetch_related('proc').all().order_by("-year","id")
	years = Proc.objects.filter().distinct().values('datetime__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Tender', 'legend': f'Tender'
	}
	return render(request, 'proc_r/dg_list.html', context)

@allowed_users(allowed_roles=['sigp_dg,sigp_admin'])
def rDGProcYear(request, year):
	group = get_roles(request)
	dg = c_user_dg(request.user)
	objects = Project.objects.filter(owner__dg=dg, proc__is_req_start=True, proc__datetime__year=year).prefetch_related('proc').all().order_by("-year","id")
	years = Proc.objects.filter().distinct().values('datetime__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Tender Tinan {year}', 'legend': f'Tender Tinan {year}'
	}
	return render(request, 'proc_r/dg_list.html', context)

@allowed_users(allowed_roles=['sigp_dg,sigp_admin'])
def rDGProcDet(request, hashid):
	group = get_roles(request)
	dg = c_user_dg(request.user)
	proj = get_object_or_404(Project, hashed=hashid)
	proc = Proc.objects.filter(project=proj).last()
	comps = ProcComp.objects.filter(proc=proc).all().order_by('best')
	letters = ProcLetter.objects.filter(project=proj).all().order_by("-date")
	context = {
		'group': group, 'proj': proj, 'proc': proc, 'comps': comps, 'letters': letters,
		'title': f'Karta Konaba Tender', 'legend': f'Karta Konaba Tender'
	}
	return render(request, 'proc_r/dg_det.html', context)
### DNA
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def rDNAProcLetDet(request, hashid):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	letdna = get_object_or_404(ProcLetter, hashed=hashid)
	proj = letdna.project
	proc = letdna.proc
	comps = ProcComp.objects.filter(proc=proc).all().order_by('best')
	if letdna.is_req == True:
		objects = ProcLetter.objects.filter((Q(is_dgaf=True)|Q(is_min=True)), proc=proc, is_req=True).all()
	else:
		objects = ProcLetter.objects.filter((Q(is_dgaf=True)|Q(is_min=True)), proc=proc, is_req=False).all()
	context = {
		'group': group, 'proj': proj, 'proc': proc, 'letdna': letdna, 'objects': objects, 'comps': comps,
		'title': 'Detalha Karta', 'legend': 'Detalha Karta',
	}
	return render(request, 'proc_r/dna_det.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def rDNAProcLetList(request):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	objects = ProcLetter.objects.filter(is_div=True).all().order_by("-date")
	years = ProcLetter.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Karta DNA Konaba Tender', 'legend': f'Karta DNA Konaba Tender'
	}
	return render(request, 'proc_r/dna_list.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def rDNAProcLetYear(request, year):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	objects = ProcLetter.objects.filter(is_div=True, date__year=year).all().order_by("-date")
	years = ProcLetter.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Karta DNA Konaba Tender Tinan {year}', 'legend': f'Karta DNA Konaba Tender Tinan {year}'
	}
	return render(request, 'proc_r/dna_list.html', context)
