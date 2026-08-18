from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from project.models import Project, ProjectEst
from finance.models import CPVReq, CPVReqTrack

#dnof
@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVReqList(request):
	group = request.user.groups.all()[0].name
	objects = CPVReq.objects.filter().all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Rekizasaun CPV', 'legend': 'Lista Rekizasaun CPV'
	}
	return render(request, 'finance_cpv/dnof_req_list.html', context)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVReqDet(request, hashid):
	group = request.user.groups.all()[0].name
	obj = get_object_or_404(CPVReq, hashed=hashid)
	proj = obj.proj
	projest = ProjectEst.objects.filter(project=proj).first()
	track = CPVReqTrack.objects.filter(cpvreq=obj).first()
	percent = 0
	if track.percent: percent = track.percent
	context = {
		'group': group, 'proj': proj, 'projest': projest,  'obj': obj, 'track': track, 'percent': percent,
		'title': 'Detallu Rekizasaun CPV', 'legend': 'Detallu  Rekizasaun CPV',
	}
	return render(request, 'finance_cpv/dnof_req_det.html', context)
# dgaf
@login_required
@allowed_users(allowed_roles=['dgaf'])
def dgafCPVReqList(request):
	group = request.user.groups.all()[0].name
	objects = CPVReq.objects.filter().all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Rekizasaun CPV', 'legend': 'Lista Rekizasaun CPV',
	}
	return render(request, 'finance_cpv/dgaf_req_list.html', context)

@login_required
@allowed_users(allowed_roles=['dgaf'])
def dgafCPVReqDet(request, hashid):
	group = request.user.groups.all()[0].name
	obj = get_object_or_404(CPVReq, hashed=hashid)
	proj = obj.proj
	projest = ProjectEst.objects.filter(project=proj).first()
	track = CPVReqTrack.objects.filter(cpvreq=obj).first()
	context = {
		'group': group, 'obj': obj, 'proj': proj, 'projest': projest, 'track': track,
		'title': 'Detallu Rekizasaun CPV', 'legend': 'Detallu Rekizasaun CPV',
	}
	return render(request, 'finance_cpv/dgaf_req_det.html', context)
# gab
@login_required
@allowed_users(allowed_roles=['gab','uivp'])
def gabCPVReqList(request):
	group = request.user.groups.all()[0].name
	objects = CPVReq.objects.filter().all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Rekizasaun CPV', 'legend': 'Lista Rekizasaun CPV',
	}
	return render(request, 'finance_cpv/gab_req_list.html', context)

@login_required
@allowed_users(allowed_roles=['gab','uivp'])
def gabCPVReqDet(request, hashid):
	group = request.user.groups.all()[0].name
	obj = get_object_or_404(CPVReq, hashed=hashid)
	proj = obj.proj
	projest = ProjectEst.objects.filter(project=proj).first()
	track = CPVReqTrack.objects.filter(cpvreq=obj).first()
	context = {
		'group': group, 'obj': obj, 'proj': proj, 'projest': projest, 'track': track,
		'title': 'Detallu Rekizasaun CPV', 'legend': 'Detallu Rekizasaun CPV',
	}
	return render(request, 'finance_cpv/gab_req_det.html', context)
#