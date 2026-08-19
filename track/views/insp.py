import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from track.models import InspJustify2
from insp.models import Insp, InspTracks
from users.decorators import allowed_users
from sigp.utils import get_roles

def trackInspList(request):
	group = get_roles(request)
	objs = Insp.objects.filter().all().order_by('-start_date')
	today = datetime.date.today()
	objects = []
	for i in objs:
		track = InspTracks.objects.filter(insp=i).first()
		percent = 0
		if track: 
			if track.percent: percent = track.percent
		if i.is_end == False:
			limit = (today-i.end_date).days
		else: limit = (track.date_end-i.end_date).days
		# if today > i.end_date: 	limit = (today-i.end_date).days
		# else: limit = (today-i.end_date).days
		objects.append([i,track,percent,limit])
	context = {
		'group': group, 'objects': objects,
		'title': 'Track Inspeksaun', 'legend': 'Track Inspeksaun'
	}
	return render(request, 'track/insp_list.html', context)

def trackInspDet(request, hashid):
	group = get_roles(request)
	insp = get_object_or_404(Insp, hashed=hashid)
	cont = insp.cont
	proj = cont.project
	track = InspTracks.objects.filter(insp=insp).first()
	today = datetime.date.today()
	if insp.is_end == False:
		# if today > ver.end_date: limit = (today-ver.end_date).days
		# else: limit = (today-ver.end_date).days
		limit = (today-insp.end_date).days
	else: limit = (track.date_end-insp.end_date).days
	percent,obj_days = 0,[]
	if track:
		if track.percent: percent = track.percent
		a,b,c,d,e,f = "","","","","",""
        #sec next
		if track.is_sec_in_1 == True and track.is_sec_out_1 == False: a = (today-track.date_sec_in_1).days
		elif track.is_sec_out_1 == True: a = (track.date_sec_out_1-track.date_sec_in_1).days
		#eng
		if track.is_eng_in == True and track.is_eng_out == False: b = (today-track.date_eng_in).days
		elif track.is_eng_out == True: b = (track.date_eng_out-track.date_eng_in).days
		#sec back
		if track.is_sec_in_2 == True and track.is_sec_out_2 == False: c = (today-track.date_sec_in_2).days
		elif track.is_sec_out_2 == True: c = (track.date_sec_out_2-track.date_sec_in_2).days
		#uvip in
		if track.is_end == True: d = (today-track.date_end).days
		elif track.is_uvip_in == True: d = (track.date_uvip_in-track.date_sec_out_2).days
		obj_days.append([a,b,c,d,e,f])
	justs = InspJustify2.objects.filter(insp=insp).all()
	context = {
		'group': group, 'cont': cont, 'proj': proj, 'insp': insp, 'track': track,
		'percent': percent, 'obj_days': obj_days, 'limit': limit, 'justs':justs,
		'title': 'Prosesu Inspeksaun', 'legend': 'Prosesu Inspeksaun'
	}
	return render(request, 'track/insp_det.html', context)