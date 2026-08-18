import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from conf.decorators import allowed_users
from project.models import Project, ProjectEst
from finance.models import CPV, CPVReq, CPVTrack, CPVLetter
from conf.user_utils import c_user_dgaf, c_user_div, c_user_dnof, c_user_dna

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVList(request):
	group = request.user.groups.all()[0].name
	objects = Project.objects.filter(is_end=False).all().order_by('-code')
	context = {
		'group':group, 'objects':objects,
		'title': 'Lista Projetu', 'legend': 'Lista Projetu',
	}
	return render(request, 'finance_cpv/dnof_cpv_list.html', context)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVDet(request, hashid):
	group = request.user.groups.all()[0].name
	proj = get_object_or_404(Project, hashed=hashid)
	projest = ProjectEst.objects.filter(project=proj).first()
	objects = CPV.objects.filter(proj=proj).all()
	context = {
		'group': group, 'proj':proj, 'projest':projest, 'objects':objects, 'todgaf':1, 'togab':2,
		'title': 'Lista CPV', 'legend': 'Lista CPV',
	}
	return render(request, 'finance_cpv/dnof_cpv_det.html', context)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVLetDet(request, hashid):
	group = request.user.groups.all()[0].name
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
@login_required
@allowed_users(allowed_roles=['dgaf','gab'])
def dgafCPVList(request):
	group = request.user.groups.all()[0].name
	objects = CPV.objects.filter().all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista CPV', 'legend': 'Lista CPV',
	}
	return render(request, 'finance_cpv/dgaf_cpv_list.html', context)

@login_required
@allowed_users(allowed_roles=['dgaf','gab'])
def dgafCPVDet(request, hashid):
	group = request.user.groups.all()[0].name
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
@login_required
@allowed_users(allowed_roles=['uivp','dna','admin'])
def uvipCPVList(request):
	group = request.user.groups.all()[0].name
	objects = CPV.objects.filter().all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista CPV', 'legend': 'Lista CPV',
	}
	return render(request, 'finance_cpv/uvip_cpv_list.html', context)

@login_required
@allowed_users(allowed_roles=['uivp','dna','admin'])
def uvipCPVDet(request, hashid):
	group = request.user.groups.all()[0].name
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