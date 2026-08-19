import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.decorators import allowed_users
from sigp.utils import get_roles
from project.models import Project, ProjectEst
from finance.models import CPV, CPVReq, CPVTrack, CPVLetter
from conf.user_utils import c_user_dgaf, c_user_div, c_user_dnof, c_user_dna

@allowed_users(allowed_roles=['sigp_admin','sigp_dnof'])
def dnofCPVList(request):
	group = get_roles(request)
	objects = Project.objects.filter(is_end=False).all().order_by('-code')
	context = {
		'group':group, 'objects':objects,
		'title': 'Lista Projetu', 'legend': 'Lista Projetu',
	}
	return render(request, 'finance_cpv/dnof_cpv_list.html', context)

@allowed_users(allowed_roles=['sigp_admin','sigp_dnof'])
def dnofCPVDet(request, hashid):
	group = get_roles(request)
	proj = get_object_or_404(Project, hashed=hashid)
	projest = ProjectEst.objects.filter(project=proj).first()
	objects = CPV.objects.filter(proj=proj).all()
	context = {
		'group': group, 'proj':proj, 'projest':projest, 'objects':objects, 'todgaf':1, 'togab':2,
		'title': 'Lista CPV', 'legend': 'Lista CPV',
	}
	return render(request, 'finance_cpv/dnof_cpv_det.html', context)

@allowed_users(allowed_roles=['sigp_admin','sigp_dnof'])
def dnofCPVLetDet(request, hashid):
	group = get_roles(request)
	cpvlet = get_object_or_404(CPVLetter, hashed=hashid)
	cpv = cpvlet.cpv
	proj = cpv.proj
	projest = ProjectEst.objects.filter(project=proj).first()
	track = CPVTrack.objects.filter(cpv=cpv).first()
	context = {
		'group': group, 'proj':proj, 'projest':projest, 'cpv':cpv, 'cpvlet':cpvlet, 'track':track,
		'title': 'Despaxu CPV', 'legend': 'Despaxu CPV',
	}
	return render(request, 'finance_cpv/dnof_cpv_let.html', context)
# dgaf

@allowed_users(allowed_roles=['sigp_admin','sigp_dgaf','sigp_gabm'])
def dgafCPVList(request):
	group = get_roles(request)
	objects = CPV.objects.filter().all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista CPV', 'legend': 'Lista CPV',
	}
	return render(request, 'finance_cpv/dgaf_cpv_list.html', context)

@allowed_users(allowed_roles=['sigp_admin','sigp_dgaf','sigp_gabm'])
def dgafCPVDet(request, hashid):
	group = get_roles(request)
	cpv = get_object_or_404(CPV, hashed=hashid)
	proj = cpv.proj
	projest = ProjectEst.objects.filter(project=proj).first()
	track = CPVTrack.objects.filter(cpv=cpv).first()
	lett = CPVLetter.objects.filter(cpv=cpv).first()
	context = {
		'group': group, 'cpv': cpv, 'proj': proj, 'projest': projest, 'track': track, 'lett':lett,
		'title': 'Detallu CPV', 'legend': 'Detallu CPV',
	}
	return render(request, 'finance_cpv/dgaf_cpv_det.html', context)
# uvip

@allowed_users(allowed_roles=['sigp_uivp','sigp_dna','sigp_admin'])
def uvipCPVList(request):
	group = get_roles(request)
	objects = CPV.objects.filter().all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista CPV', 'legend': 'Lista CPV',
	}
	return render(request, 'finance_cpv/uvip_cpv_list.html', context)

@allowed_users(allowed_roles=['sigp_uivp','sigp_dna','sigp_admin'])
def uvipCPVDet(request, hashid):
	group = get_roles(request)
	cpv = get_object_or_404(CPV, hashed=hashid)
	proj = cpv.proj
	projest = ProjectEst.objects.filter(project=proj).first()
	track = CPVTrack.objects.filter(cpv=cpv).first()
	context = {
		'group': group, 'cpv':cpv, 'proj': proj, 'projest': projest, 'track': track,
		'title': 'Detallu CPV', 'legend': 'Detallu CPV',
	}
	return render(request, 'finance_cpv/uvip_cpv_det.html', context)
#