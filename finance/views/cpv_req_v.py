from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from project.models import Project, ProjectEst
from finance.models import CPVReq, CPVReqTrack


#dnof
@allowed_users(allowed_roles=['sigp_admin','sigp_dnof'])
def dnofCPVReqList(request):
	group = get_roles(request)
	objects = CPVReq.objects.filter().all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Rekizasaun CPV', 'legend': 'Lista Rekizasaun CPV'
	}
	return render(request, 'finance_cpv/dnof_req_list.html', context)

@allowed_users(allowed_roles=['sigp_admin','sigp_dnof'])
def dnofCPVReqDet(request, hashid):
	group = get_roles(request)
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
@allowed_users(allowed_roles=['sigp_admin','sigp_dgaf'])
def dgafCPVReqList(request):
	group = get_roles(request)
	objects = CPVReq.objects.filter().all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Rekizasaun CPV', 'legend': 'Lista Rekizasaun CPV',
	}
	return render(request, 'finance_cpv/dgaf_req_list.html', context)

@allowed_users(allowed_roles=['sigp_admin','sigp_dgaf'])
def dgafCPVReqDet(request, hashid):
	group = get_roles(request)
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

@allowed_users(allowed_roles=['sigp_admin','sigp_uivp','sigp_gabm'])
def gabCPVReqList(request):
	group = get_roles(request)
	objects = CPVReq.objects.filter().all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Rekizasaun CPV', 'legend': 'Lista Rekizasaun CPV',
	}
	return render(request, 'finance_cpv/gab_req_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_uivp','sigp_gabm'])
def gabCPVReqDet(request, hashid):
	group = get_roles(request)
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