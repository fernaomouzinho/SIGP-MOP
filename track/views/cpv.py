import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from project.models import Project
from finance.models import CPVReq, CPVReqTrack, CPV, CPVTrack
from track.models import CPVJustify, CPVReqJustify
from users.decorators import allowed_users
from sigp.utils import get_roles


def trackCPVReqList(request):
	group = get_roles(request)
	objs = CPVReq.objects.filter(proj__is_end=False).all().order_by('id')
	objects = []
	for i in objs:
		track = CPVReqTrack.objects.filter(cpvreq=i).first()
		objects.append([i,track])
	context = {
		'group': group, 'objects': objects,
		'title': 'Track Rekizasaun CPV', 'legend': 'Track Rekizasaun CPV'
	}
	return render(request, 'track/cpvreq_list.html', context)


def trackCPVReqDet(request, hashid):
	group = get_roles(request)
	cpvreq = get_object_or_404(CPVReq, hashed=hashid)
	proj = cpvreq.proj
	track = CPVReqTrack.objects.filter(cpvreq=cpvreq).first()
	today = datetime.date.today()
	percent,obj_days = 0,[]
	percent = 0
	if track:
		if track.percent: percent = track.percent
		a,b,c,d = 0,0,0,0
		if track.is_dnof_out == True and track.is_dgaf_in == False: a = (today-track.date_dnof_out).days
		elif track.is_dgaf_in == True: a = (track.date_dgaf_in-track.date_dnof_out).days
		if track.is_appr == True and track.is_end == False: b = (today-track.date_appr).days
		elif track.is_end == True: b = (track.date_end-track.date_appr).days
		total = a+b+c+d
		obj_days.append([a,b,c,d,total])
	justs = CPVReqJustify.objects.filter(cpvreq=cpvreq).all()
	context = {
		'group':group, 'proj':proj, 'cpvreq':cpvreq, 'track':track, 'percent':percent,
		'obj_days': obj_days, 'justs': justs,
		'title': 'Track Rekizasaun CPV', 'legend': 'Track Rekizasaun CPV'
	}
	return render(request, 'track/cpvreq_det.html', context)
#

def trackCPVList(request):
	group = get_roles(request)
	objs = CPV.objects.filter(proj__is_end=False).all().order_by('id')
	objects = []
	for i in objs:
		track = CPVTrack.objects.filter(cpv=i).first()
		objects.append([i,track])
	context = {
		'group': group, 'objects': objects,
		'title': 'Track CPV', 'legend': 'Track CPV'
	}
	return render(request, 'track/cpv_list.html', context)


def trackCPVDet(request, hashid):
	group = get_roles(request)
	cpv = get_object_or_404(CPV, hashed=hashid)
	proj = cpv.proj
	track = CPVTrack.objects.filter(cpv=cpv).first()
	today = datetime.date.today()
	percent,obj_days = 0,[]
	percent = 0
	if track:
		if track.percent: percent = track.percent
		a,b,c,d = 0,0,0,0
		if track.is_dnof_out == True and track.is_dgaf_in == False: 
			a = (today-track.date_dnof_out).days
		elif track.is_dgaf_in == True and track.is_appr == False: 
			a = (track.date_dgaf_in-track.date_dnof_out).days
		elif track.is_appr == True and track.is_dgaf_out == False: 
			a = (track.date_appr-track.date_dgaf_in).days
		elif track.is_dgaf_out == True: 
			a = (track.date_dgaf_out-track.date_dgaf_in).days
		if track.is_dgaf_out == True and track.is_dnof_in == False: 
			b = (today-track.date_dgaf_out).days
		elif track.is_dnof_in == True and track.is_end == False:
			b = (track.date_dnof_in-track.date_dgaf_out).days
		elif track.is_end == True:
			b = (track.date_end-track.date_dnof_in).days
		total = a+b+c+d
		obj_days.append([a,b,c,d,total])
	justs = CPVJustify.objects.filter(cpv=cpv).all()
	context = {
		'group':group, 'proj':proj, 'cpv':cpv, 'track':track, 'percent':percent,
		'obj_days':obj_days, 'justs':justs,
		'title': 'Track CPV', 'legend': 'Track CPV'
	}
	return render(request, 'track/cpv_det.html', context)
